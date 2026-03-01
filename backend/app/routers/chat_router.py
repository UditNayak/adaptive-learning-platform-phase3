from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.dtos.chat_dto import ChatCreateDTO, ChatMessageCreateDTO, ChatSessionResponseDTO
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/create", response_model=ChatSessionResponseDTO)
def create_chat(data: ChatCreateDTO, db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.create_chat(
        user_id=data.user_id,
        topic_name=data.topic_name,
        topic_description=data.topic_description,
        knowledge_level=data.knowledge_level
    )


@router.post("/message")
def send_message(data: ChatMessageCreateDTO, db: Session = Depends(get_db)):
    service = ChatService(db)
    return service.send_message(
        chat_session_id=data.chat_session_id,
        content=data.content,
        reply_to_message_id=data.reply_to_message_id
    )