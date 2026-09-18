from typing import AsyncGenerator  # noqa: UP035

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
