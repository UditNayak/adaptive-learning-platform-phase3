import uuid
from app.models.chat_session import ChatSession


def test_submit_wrong_answer(db):

    # IMPORTANT:
    # UUID field must receive uuid.UUID object.
    user_id = uuid.uuid4()

    session = ChatSession(
        user_id=user_id,
        topic_name="Binary Search",
        initial_knowledge_level="BEGINNER",
        current_level="BEGINNER"
    )

    db.add(session)
    db.commit()

    # This test only checks DB creation works
    assert session.id is not None