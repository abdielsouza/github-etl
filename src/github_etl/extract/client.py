from __future__ import annotations
import dotenv
import os
import httpx

class GithubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        dotenv.load_dotenv()
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {os.getenv("GITHUB_TOKEN", "")}",
            },
            timeout=30,
        )
    
    async def get(self, endpoint: str):
        response = await self._client.get(endpoint)
        response.raise_for_status()

        return response.json()

    async def close(self):
        await self._client.aclose()