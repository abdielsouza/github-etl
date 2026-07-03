from github_etl.analytics.base import Analytics

class LanguageAnalytics(Analytics):
    def distribution(self):
        return self._warehouse.query(
            """
            SELECT language, COUNT(*) repositories, SUM(stars) stars, SUM(forks) forks
            FROM repositories
            GROUP BY language
            ORDER BY stars DESC
            """
        )