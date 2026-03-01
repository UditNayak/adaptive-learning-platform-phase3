from sqlalchemy.orm import Session
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage


class ChatRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_session(self, session: ChatSession):
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def create_message(self, message: ChatMessage):
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_message(self, message_id):
        return self.db.query(ChatMessage).filter(ChatMessage.id == message_id).first()