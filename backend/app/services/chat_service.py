from sqlalchemy.orm import Session
from app.repositories.chat_repo import ChatRepository
from app.models.chat_session import ChatSession, KnowledgeLevel
from app.models.chat_message import ChatMessage, MessageRole, MessageType
from app.llm.factory import get_llm_provider
from app.llm.prompt_builder import build_explanation_prompt
from app.llm.response_parser import parse_explanation_response


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

        prompt = build_explanation_prompt(
            topic_name=topic_name,
            knowledge_level=knowledge_level,
            description=topic_description
        )

        raw_response = self.llm.generate(
            messages=[{"role": "user", "content": prompt}]
        )

        parsed = parse_explanation_response(raw_response)

        session.title = parsed.get("title")
        self.repo.db.commit()
        self.repo.db.refresh(session)

        message = ChatMessage(
            chat_session_id=session.id,
            role=MessageRole.ASSISTANT,
            message_type=MessageType.EXPLANATION,
            content=parsed.get("explanation")
        )

        self.repo.create_message(message)

        return session

    def send_message(self, chat_session_id, content, reply_to_message_id=None):

        # Save user message first
        user_message = ChatMessage(
            chat_session_id=chat_session_id,
            role=MessageRole.USER,
            message_type=MessageType.GENERAL,
            content=content,
            reply_to_message_id=reply_to_message_id
        )

        self.repo.create_message(user_message)

        # Build prompt
        if reply_to_message_id:
            referenced = self.repo.get_message(reply_to_message_id)

            if referenced:
                prompt = f"""
    User is replying to the following message:

    ----------------------
    {referenced.content}
    ----------------------

    User question:
    {content}
    """
            else:
                prompt = content
        else:
            prompt = content

        # Send to LLM
        response = self.llm.generate(
            messages=[{"role": "user", "content": prompt}]
        )

        assistant_message = ChatMessage(
            chat_session_id=chat_session_id,
            role=MessageRole.ASSISTANT,
            message_type=MessageType.GENERAL,
            content=response
        )

        return self.repo.create_message(assistant_message)