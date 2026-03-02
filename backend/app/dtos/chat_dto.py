from pydantic import BaseModel
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime


class ChatCreateDTO(BaseModel):
    user_id: UUID
    topic_name: str
    topic_description: Optional[str] = None
    knowledge_level: str


class ChatMessageCreateDTO(BaseModel):
    chat_session_id: UUID
    content: str
    reply_to_message_id: Optional[UUID] = None


class ChatSessionResponseDTO(BaseModel):
    id: UUID
    user_id: UUID
    topic_name: str
    topic_description: Optional[str]
    initial_knowledge_level: str
    current_level: str
    title: Optional[str]

    class Config:
        from_attributes = True


class ChatSessionListDTO(BaseModel):
    id: UUID
    topic_name: str
    title: Optional[str]
    current_level: str
    created_at: datetime

    class Config:
        from_attributes = True