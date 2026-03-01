from sqlalchemy.orm import Session
from app.repositories.chat_repo import ChatRepository
from app.models.chat_session import ChatSession, KnowledgeLevel
from app.models.chat_message import ChatMessage, MessageRole, MessageType
from app.llm.factory import get_llm_provider


class ChatService:

    def __init__(self, db: Session):
        self.repo = ChatRepository(db)
        self.llm = get_llm_provider()

    def create_chat(self, user_id, topic_name, topic_description, knowledge_level):

        session = ChatSession(
            user_id=user_id,
            topic_name=topic_name,
            topic_description=topic_description,
            initial_knowledge_level=KnowledgeLevel(knowledge_level),
            current_level=KnowledgeLevel(knowledge_level)
        )

        session = self.repo.create_session(session)

        prompt = f"""
        Explain the topic '{topic_name}' for a {knowledge_level} level student.
        {topic_description or ""}
        """

        response = self.llm.generate(
            messages=[{"role": "user", "content": prompt}]
        )

        message = ChatMessage(
            chat_session_id=session.id,
            role=MessageRole.ASSISTANT,
            message_type=MessageType.EXPLANATION,
            content=response
        )

        self.repo.create_message(message)

        return session

    def send_message(self, chat_session_id, content, reply_to_message_id=None):

        user_message = ChatMessage(
            chat_session_id=chat_session_id,
            role=MessageRole.USER,
            message_type=MessageType.GENERAL,
            content=content,
            reply_to_message_id=reply_to_message_id
        )

        self.repo.create_message(user_message)

        messages = [{"role": "user", "content": content}]

        response = self.llm.generate(messages=messages)

        assistant_message = ChatMessage(
            chat_session_id=chat_session_id,
            role=MessageRole.ASSISTANT,
            message_type=MessageType.GENERAL,
            content=response
        )

        return self.repo.create_message(assistant_message)