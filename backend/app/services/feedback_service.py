from app.models.message_feedback import MessageFeedback
from app.repositories.feedback_repo import FeedbackRepository


class FeedbackService:

    def __init__(self, db):
        self.repo = FeedbackRepository(db)

    def submit_feedback(self, message_id, is_helpful, feedback_text=None):

        feedback = MessageFeedback(
            message_id=message_id,
            is_helpful=is_helpful,
            feedback_text=feedback_text
        )

        return self.repo.create_feedback(feedback)