from sqlalchemy import Column, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_entity import BaseEntity


class MessageFeedback(BaseEntity):
    __tablename__ = "message_feedback"

    message_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_messages.id"),
        nullable=False
    )

    is_helpful = Column(Boolean, nullable=False)

    feedback_text = Column(Text, nullable=True)