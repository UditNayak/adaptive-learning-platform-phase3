from sqlalchemy.orm import Session

from app.llm.factory import get_llm_provider
from app.llm.prompt_builder import build_quiz_prompt
from app.llm.response_parser import parse_quiz_response

from app.repositories.quiz_repo import QuizRepository
from app.services.progress_service import ProgressService
from app.models.chat_session import ChatSession
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.chat_message import ChatMessage, MessageRole, MessageType


class QuizService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = QuizRepository(db)
        self.llm = get_llm_provider()

    def generate_quiz(self, chat_session):

        prompt = build_quiz_prompt(
            topic_name=chat_session.topic_name,
            level=chat_session.current_level.value
        )

        raw = self.llm.generate([{"role": "user", "content": prompt}])
        parsed = parse_quiz_response(raw)

        quiz = Quiz(
            chat_session_id=chat_session.id,
            question_text=parsed["question"],
            options_json=parsed["options"],
            correct_option=parsed["correct_option"],
            difficulty=chat_session.current_level.value,
            points=parsed["points"],
            hint=parsed.get("hint"),
            explanation=parsed.get("explanation")
        )

        quiz = self.repo.create_quiz(quiz)

        # Save chat message referencing quiz
        message = ChatMessage(
            chat_session_id=chat_session.id,
            role=MessageRole.ASSISTANT,
            message_type=MessageType.QUIZ,
            content="Quiz generated",
            metadata_json={
                "quiz_id": str(quiz.id)
            }
        )

        self.db.add(message)
        self.db.commit()

        return quiz

    def submit_answer(self, quiz_id, user_id, selected_option):

        quiz = self.repo.get_quiz(quiz_id)

        is_correct = selected_option == quiz.correct_option
        points = quiz.points if is_correct else 0

        attempt = QuizAttempt(
            quiz_id=quiz.id,
            user_id=user_id,
            selected_option=selected_option,
            is_correct=is_correct,
            points_awarded=points
        )

        self.repo.create_attempt(attempt)

        # Update topic progress
        session = self.db.query(ChatSession).filter(
            ChatSession.id == quiz.chat_session_id
        ).first()

        progress_service = ProgressService(self.db)
        progress = progress_service.update_progress(
            user_id=user_id,
            topic_name=session.topic_name,
            points_awarded=points,
            is_correct=is_correct
        )

        # Sync session level
        session.current_level = progress.current_level
        self.db.commit()

        return {
            "correct": is_correct,
            "points_awarded": points,
            "explanation": quiz.explanation,
            "hint": None if is_correct else quiz.hint,
            "new_level": progress.current_level,
            "total_points": progress.total_points
        }