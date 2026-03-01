import enum

from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.models.base_entity import BaseEntity


class KnowledgeLevel(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    PRO = "PRO"


class ChatSession(BaseEntity):
    __tablename__ = "chat_sessions"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    topic_name = Column(String, nullable=False)
    topic_description = Column(String, nullable=True)

    initial_knowledge_level = Column(Enum(KnowledgeLevel, native_enum=False), nullable=False)

    current_level = Column(Enum(KnowledgeLevel, native_enum=False), nullable=False)

    title = Column(String, nullable=True)