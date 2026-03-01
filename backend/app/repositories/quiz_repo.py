from sqlalchemy.orm import Session
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt


class QuizRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_quiz(self, quiz: Quiz):
        self.db.add(quiz)
        self.db.commit()
        self.db.refresh(quiz)
        return quiz

    def get_quiz(self, quiz_id):
        return self.db.query(Quiz).filter(Quiz.id == quiz_id).first()

    def create_attempt(self, attempt: QuizAttempt):
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt