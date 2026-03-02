import pytest
import warnings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from app.main import app as fastapi_app
from app.db.dependencies import get_db
from app.db.base import Base

# Import the factory module itself
import app.llm.factory as llm_factory

# Force model imports
import app.models.user
import app.models.chat_session
import app.models.chat_message
import app.models.quiz
import app.models.quiz_attempt
import app.models.topic_progress
import app.models.message_feedback


# Suppress Pydantic warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Shared SQLite memory DB
SQLALCHEMY_DATABASE_URL = "sqlite:///file::memory:?cache=shared"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False, "uri": True},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class MockLLMProvider:

    def generate(self, messages):
        return """
        {
            "title": "Mock Title",
            "explanation": "Mock Explanation",
            "key_points": ["Point 1", "Point 2"]
        }
        """


@pytest.fixture(autouse=True)
def override_llm():
    """
    Automatically override get_llm_provider for all tests.
    Prevents real API calls.
    """

    original_function = llm_factory.get_llm_provider

    def mock_get_llm_provider():
        return MockLLMProvider()

    llm_factory.get_llm_provider = mock_get_llm_provider

    yield

    llm_factory.get_llm_provider = original_function


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):

    def override_get_db():
        try:
            yield db
        finally:
            pass

    fastapi_app.dependency_overrides[get_db] = override_get_db

    with TestClient(fastapi_app) as c:
        yield c

    fastapi_app.dependency_overrides.clear()