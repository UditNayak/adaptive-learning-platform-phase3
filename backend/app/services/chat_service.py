from sqlalchemy.orm import Session
from app.repositories.chat_repo import ChatRepository
from app.repositories.quiz_repo import QuizRepository
from app.models.chat_session import ChatSession, KnowledgeLevel
from app.models.chat_message import ChatMessage, MessageRole, MessageType
from app.llm.factory import get_llm_provider
from app.llm.prompt_builder import build_explanation_prompt
from app.llm.response_parser import parse_explanation_response


class ChatService:

    def __init__(self, db: Session):
        self.repo = ChatRepository(db)
        self.llm = get_llm_provider()

    def create_chat(self, user_id, topic_name, topic_description, knowledge_level):

        session = ChatSession(
            user_id=user_id,
            topic_name=topic_name,
            topic_description=topic_description,
            initial_knowledge_level=KnowledgeLevel(knowledge_level),
            current_level=KnowledgeLevel(knowledge_level)
        )

        session = self.repo.create_session(session)

        prompt = build_explanation_prompt(
            topic_name=topic_name,
            knowledge_level=knowledge_level,
            description=topic_description
        )

        raw_response = self.llm.generate(
            messages=[{"role": "user", "content": prompt}]
        )

        parsed = parse_explanation_response(raw_response)

        session.title = parsed.get("title")
        self.repo.db.commit()
        self.repo.db.refresh(session)

        message = ChatMessage(
            chat_session_id=session.id,
            role=MessageRole.ASSISTANT,
            message_type=MessageType.EXPLANATION,
            content=parsed.get("explanation"),
            metadata_json={
                "references": parsed.get("references", [])
            }
        )

        self.repo.create_message(message)

        return session

    def list_user_sessions(self, user_id):
        return self.repo.get_user_sessions(user_id)

    def get_chat_session_detail(self, chat_session_id):
        return self.repo.get_session(chat_session_id)

    def get_conversation(self, chat_session_id, user_id):

        messages = self.repo.get_session_messages(chat_session_id)
        quiz_repo = QuizRepository(self.repo.db)

        conversation = []

        for msg in messages:

            item = {
                "id": msg.id,
                "role": msg.role.value,
                "message_type": msg.message_type.value,
                "content": msg.content,
                "created_at": msg.created_at,
                "metadata_json": msg.metadata_json,
                "quiz_data": None
            }

            if msg.message_type == MessageType.QUIZ and msg.metadata_json:

                quiz_id = msg.metadata_json.get("quiz_id")

                if quiz_id:
                    quiz = quiz_repo.get_quiz(quiz_id)
                    attempt = quiz_repo.get_attempt_for_user(quiz_id, user_id)

                    item["quiz_data"] = {
                        "question": quiz.question_text,
                        "options": quiz.options_json,
                        "correct_option": quiz.correct_option,
                        "difficulty": quiz.difficulty,
                        "points": quiz.points,
                        "hint": quiz.hint,
                        "explanation": quiz.explanation,
                        "selected_option": attempt.selected_option if attempt else None,
                        "is_correct": attempt.is_correct if attempt else None,
                        "points_awarded": attempt.points_awarded if attempt else None
                    }

            conversation.append(item)

        return conversation

    def send_message(self, chat_session_id, content, reply_to_message_id=None):

        # Save user message first
        user_message = ChatMessage(
            chat_session_id=chat_session_id,
            role=MessageRole.USER,
            message_type=MessageType.GENERAL,
            content=content,
            reply_to_message_id=reply_to_message_id
        )

        self.repo.create_message(user_message)

        # Build prompt
        if reply_to_message_id:
            referenced = self.repo.get_message(reply_to_message_id)

            if referenced:
                prompt = f"""
    User is replying to the following message:

    ----------------------
    {referenced.content}
    ----------------------

    User question:
    {content}
    """
            else:
                prompt = content
        else:
            prompt = content

        # Send to LLM
        response = self.llm.generate(
            messages=[{"role": "user", "content": prompt}]
        )

        assistant_message = ChatMessage(
            chat_session_id=chat_session_id,
            role=MessageRole.ASSISTANT,
            message_type=MessageType.GENERAL,
            content=response
        )

        return self.repo.create_message(assistant_message)