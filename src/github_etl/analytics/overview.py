from .base import Analytics

class OverviewAnalytics(Analytics):
    def summary(self):
        return self._warehouse.query(
            """
            SELECT
                COUNT(*) repositories,
                COUNT(DISTINCT owner) owners,
                COUNT(DISTINCT language) languages,
                SUM(stars) stars,
                SUM(forks) forks,
                SUM(watchers) watchers,
                SUM(open_issues) issues
            FROM repositories
            """
        )