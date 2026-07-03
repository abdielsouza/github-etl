from .base import Analytics

class RepositoryAnalytics(Analytics):
    def all(self):
        return self._warehouse.query("SELECT * FROM repositories")

    def top_starred(self, limit: int = 10):
        return self._warehouse.query(
            f"""
            SELECT owner, name, stars FROM repositories
            ORDER BY forks DESC
            LIMIT {limit}
            """
        )
    
    def newest(self):
        return self._warehouse.query(
            """
            SELECT * FROM repositories
            ORDER BY created_at DESC
            """
        )

    def recently_updated(self):
        return self._warehouse.query(
            """
            SELECT * FROM repositories
            ORDER BY updated_at DESC
            """
        )