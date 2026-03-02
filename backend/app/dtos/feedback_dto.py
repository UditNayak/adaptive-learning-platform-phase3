from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class MessageFeedbackCreateDTO(BaseModel):
    message_id: UUID
    is_helpful: bool
    feedback_text: Optional[str] = None


class MessageFeedbackResponseDTO(BaseModel):
    id: UUID
    message_id: UUID
    is_helpful: bool
    feedback_text: Optional[str]

    class Config:
        from_attributes = True