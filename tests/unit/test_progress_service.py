import uuid
from app.services.progress_service import ProgressService


def test_level_upgrade(db):

    service = ProgressService(db)

    # IMPORTANT:
    # UUID columns require real uuid.UUID objects,
    # not strings. Passing string causes ".hex" error.
    user_id = uuid.uuid4()

    progress = service.update_progress(
        user_id = user_id,
        topic_name="Binary Search",
        points_awarded=60,
        is_correct=True
    )

    assert progress.current_level == "INTERMEDIATE"