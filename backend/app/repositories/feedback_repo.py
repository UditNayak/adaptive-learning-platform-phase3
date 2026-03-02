from sqlalchemy.orm import Session
from app.models.message_feedback import MessageFeedback


class FeedbackRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_feedback(self, feedback: MessageFeedback):
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback