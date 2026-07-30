"""
Base HTTP Client
"""

import httpx
from app.config import settings


class BaseClient:

    def __init__(self):

        self.timeout = httpx.Timeout(30)

        self.client = httpx.AsyncClient(
            timeout=self.timeout,
            verify=True
        )

    async def get(
        self,
        url: str,
        params=None,
        headers=None
    ):

        response = await self.client.get(
            url,
            params=params,
            headers=headers
        )

        response.raise_for_status()

        return response.json()

    async def post(
        self,
        url,
        json=None,
        headers=None
    ):

        response = await self.client.post(
            url,
            json=json,
            headers=headers
        )

        response.raise_for_status()

        return response.json()

    async def close(self):

        await self.client.aclose()