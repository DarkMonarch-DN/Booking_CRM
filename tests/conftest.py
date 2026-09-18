import asyncio  # noqa: F401
from datetime import datetime
from typing import AsyncGenerator  # noqa: UP035

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine

from app.core.database import Base
from app.dependencies.db import get_db_session
from app.main import app
from app.models.booking import Booking
from app.models.item import Item, ItemStatus, ItemType
from app.models.user import User, UserRole
from app.utils.user import encode_jwt

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_crm"

# Создаем один глобальный движок
engine = create_async_engine(TEST_DATABASE_URL, echo=False)


# Указываем anyio в качестве бэкенда по умолчанию
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(anyio_backend):
    """
    Создает таблицы ОДИН РАЗ перед началом всех тестов.
    После прохождения тестов они не удаляются, так как транзакции ниже
    все равно откатят любые изменения в данных!
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture(scope="session")
async def connection(anyio_backend) -> AsyncGenerator[AsyncConnection, None]:
    """Открывает ОДНО соединение с БД на все тесты."""
    async with engine.connect() as conn:
        yield conn


@pytest.fixture(scope="function")
async def transaction(connection: AsyncConnection):
    """Создает корневую транзакцию для каждого теста."""
    async with connection.begin() as trans:
        yield trans
        await trans.rollback()


@pytest.fixture(scope="function")
async def client(
    connection: AsyncConnection, transaction
) -> AsyncGenerator[AsyncClient, None]:
    """
    Создает HTTPX клиент и подменяет get_db_session.
    Использует join_transaction_mode="create_savepoint", чтобы
    FastAPI работал внутри транзакции теста, но думал, что делает коммиты.
    """

    async def _override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
            expire_on_commit=False,
        )
        async with async_session:
            yield async_session

    app.dependency_overrides[get_db_session] = _override_get_db_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def create_user(connection):
    """
    Фабрика для создания пользователей.
    Возвращает функцию, которую можно вызывать внутри тестов с любыми параметрами.
    """
    created_users = []

    async def _create_user(
        username: str, email: str, hashed_password: str, role: str = "user"
    ) -> User:
        session = AsyncSession(
            bind=connection, join_transaction_mode="create_savepoint"
        )

        user = User(
            username=username,
            email=email,
            hashed_password="hashed_123456",
            role=role,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        created_users.append(user)
        return user

    yield _create_user


@pytest.fixture(scope="function")
async def user_client(client, create_user) -> AsyncClient:
    """Клиент, авторизованный под ОБЫЧНЫМ пользователем."""
    user = await create_user(
        username="regular_user",
        email="user@crm.com",
        hashed_password="fake-hash+xyz",
        role=UserRole.regular,
    )

    token = encode_jwt({"sub": str(user.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture(scope="function")
async def admin_client(client, create_user) -> AsyncClient:
    """Клиент, авторизованный под АДМИНИСТРАТОРОМ."""
    admin = await create_user(
        username="admin_user",
        email="admin@crm.com",
        hashed_password="fake-hash+xyz",
        role=UserRole.admin,
    )

    token = encode_jwt({"sub": str(admin.id)})
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture(scope="function")
async def create_item(connection):
    created_items = []

    async def _create_item(
        number: str, type: ItemType, status: ItemStatus = ItemStatus.active
    ) -> Item:
        session = AsyncSession(
            bind=connection, join_transaction_mode="create_savepoint"
        )

        item = Item(number=number, type=type, status=status)

        session.add(item)
        await session.commit()
        await session.refresh(item)

        created_items.append(item)

        return item

    yield _create_item


@pytest.fixture(scope="function")
async def create_booking(connection):
    created_bookings = []

    async def _create_booking(
        item_id: int, time_start: datetime, time_end: datetime
    ) -> Booking:
        session = AsyncSession(
            bind=connection, join_transaction_mode="create_savepoint"
        )

        booking = Booking(item_id=item_id, time_start=time_start, time_end=time_end)

        session.add(booking)
        await session.commit()
        await session.refresh(booking)

        created_bookings.append(booking)

        return booking

    yield _create_booking
