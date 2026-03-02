from sqlalchemy.orm import Session
from app.models.chat_session import ChatSession
from app.search.factory import get_search_provider


class ReferenceService:

    def __init__(self, db: Session):
        self.db = db
        self.search = get_search_provider()

    def get_references(self, chat_session_id):
        """
        Fetch reference materials (articles + videos) for a chat session's topic.

        Queries SearXNG twice:
        - category 'general' for articles/tutorials
        - category 'videos' for YouTube and other video results
        """

        session = self.db.query(ChatSession).filter(
            ChatSession.id == chat_session_id
        ).first()

        if not session:
            raise ValueError("Chat session not found")

        query = f"{session.topic_name} tutorial"

        articles = self.search.search(query, categories="general", num_results=3)
        videos = self.search.search(query, categories="videos", num_results=2)

        return {
            "topic_name": session.topic_name,
            "articles": articles,
            "videos": videos,
        }
