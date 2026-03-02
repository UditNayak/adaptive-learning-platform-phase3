from app.repositories.analytics_repo import AnalyticsRepository


class AnalyticsService:

    def __init__(self, db):
        self.repo = AnalyticsRepository(db)

    def get_user_analytics(self, user_id):

        progresses = self.repo.get_user_progress(user_id)

        topic_data = []
        total_points = 0
        total_attempted = 0
        total_correct = 0

        for progress in progresses:
            accuracy = 0.0
            if progress.quizzes_attempted > 0:
                accuracy = (
                    progress.quizzes_correct / progress.quizzes_attempted
                ) * 100

            topic_data.append({
                "topic_name": progress.topic_name,
                "current_level": progress.current_level,
                "total_points": progress.total_points,
                "quizzes_attempted": progress.quizzes_attempted,
                "quizzes_correct": progress.quizzes_correct,
                "accuracy_percentage": round(accuracy, 2)
            })

            total_points += progress.total_points
            total_attempted += progress.quizzes_attempted
            total_correct += progress.quizzes_correct

        overall_accuracy = 0.0
        if total_attempted > 0:
            overall_accuracy = (total_correct / total_attempted) * 100

        return {
            "total_topics": len(progresses),
            "total_points": total_points,
            "total_quizzes_attempted": total_attempted,
            "total_quizzes_correct": total_correct,
            "overall_accuracy_percentage": round(overall_accuracy, 2),
            "topics": topic_data
        }