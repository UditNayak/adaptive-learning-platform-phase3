# Import all models here so that SQLAlchemy registers them

from app.models.user import User
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.topic_progress import TopicProgress