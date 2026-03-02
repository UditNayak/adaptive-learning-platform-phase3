import uuid
from app.services.progress_service import ProgressService
from app.services.analytics_service import AnalyticsService


def test_accuracy_calculation(db):

    user_id = uuid.uuid4()

    progress_service = ProgressService(db)

    # IMPORTANT:
    # Must use uuid.UUID object, not string.
    progress_service.update_progress(
        user_id=user_id,
        topic_name="Binary Search",
        points_awarded=10,
        is_correct=True
    )

    analytics = AnalyticsService(db)
    result = analytics.get_user_analytics(user_id)

    assert result["total_quizzes_correct"] == 1
    assert result["overall_accuracy_percentage"] == 100.0