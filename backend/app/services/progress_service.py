from app.repositories.progress_repo import ProgressRepository
from app.models.topic_progress import TopicProgress


class ProgressService:

    LEVEL_THRESHOLDS = {
        "BEGINNER": 0,
        "INTERMEDIATE": 50,
        "PRO": 150
    }

    def __init__(self, db):
        self.repo = ProgressRepository(db)

    def update_progress(self, user_id, topic_name, points_awarded, is_correct):

        progress = self.repo.get_progress(user_id, topic_name)

        if not progress:
            progress = TopicProgress(
                user_id=user_id,
                topic_name=topic_name,
                current_level="BEGINNER",
                total_points=0,
                quizzes_attempted=0,
                quizzes_correct=0
            )
            progress = self.repo.create_progress(progress)

        progress.quizzes_attempted += 1

        if is_correct:
            progress.quizzes_correct += 1
            progress.total_points += points_awarded

        # Check level upgrade
        progress.current_level = self._determine_level(progress.total_points)

        return self.repo.save(progress)

    def _determine_level(self, total_points):

        if total_points >= self.LEVEL_THRESHOLDS["PRO"]:
            return "PRO"

        if total_points >= self.LEVEL_THRESHOLDS["INTERMEDIATE"]:
            return "INTERMEDIATE"

        return "BEGINNER"