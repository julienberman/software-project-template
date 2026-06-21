from psycopg_pool import AsyncConnectionPool

from app.exceptions.service_exceptions import (
    ExternalServiceError,
    RepositoryError,
)

class ExampleService:
    def __init__(self, pool: AsyncConnectionPool) -> None:
        self.pool = pool

    async def get_item(
        self,
        id: int
    ) -> Item:
        pass

    async def create_item(
        self,
        name: str,
        desc: str
    ) -> Item:
        pass


