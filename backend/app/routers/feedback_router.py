from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dtos.feedback_dto import MessageFeedbackCreateDTO, MessageFeedbackResponseDTO
from app.services.feedback_service import FeedbackService

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=MessageFeedbackResponseDTO)
def submit_feedback(data: MessageFeedbackCreateDTO, db: Session = Depends(get_db)):
    service = FeedbackService(db)

    return service.submit_feedback(
        message_id=data.message_id,
        is_helpful=data.is_helpful,
        feedback_text=data.feedback_text
    )