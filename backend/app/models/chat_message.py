import enum

from sqlalchemy import Column, String, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.models.base_entity import BaseEntity


class MessageRole(str, enum.Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class MessageType(str, enum.Enum):
    EXPLANATION = "EXPLANATION"
    DOUBT = "DOUBT"
    QUIZ = "QUIZ"
    GENERAL = "GENERAL"


class ChatMessage(BaseEntity):
    __tablename__ = "chat_messages"

    chat_session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False)

    role = Column(Enum(MessageRole, native_enum=False), nullable=False)

    message_type = Column(Enum(MessageType, native_enum=False), nullable=False)

    content = Column(Text, nullable=False)

    reply_to_message_id = Column(UUID(as_uuid=True), ForeignKey("chat_messages.id"), nullable=True)

    metadata_json = Column(JSONB, nullable=True)