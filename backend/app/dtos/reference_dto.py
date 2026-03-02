from pydantic import BaseModel
from uuid import UUID
from typing import List


class ReferenceRequestDTO(BaseModel):
    chat_session_id: UUID


class ReferenceItemDTO(BaseModel):
    title: str
    url: str
    snippet: str


class ReferenceResponseDTO(BaseModel):
    topic_name: str
    articles: List[ReferenceItemDTO]
    videos: List[ReferenceItemDTO]
