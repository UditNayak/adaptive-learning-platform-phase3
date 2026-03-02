from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base_entity import BaseEntity


class TopicProgress(BaseEntity):
    __tablename__ = "topic_progress"

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    topic_name = Column(String, nullable=False)

    total_points = Column(Integer, default=0)
    current_level = Column(String, nullable=False)

    quizzes_attempted = Column(Integer, default=0)
    quizzes_correct = Column(Integer, default=0)