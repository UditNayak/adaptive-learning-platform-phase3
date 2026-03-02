from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Dict, Any
from datetime import datetime


class ConversationItemDTO(BaseModel):
    id: UUID
    role: str
    message_type: str
    content: str
    created_at: datetime

    metadata_json: Optional[Dict[str, Any]] = None
    quiz_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True