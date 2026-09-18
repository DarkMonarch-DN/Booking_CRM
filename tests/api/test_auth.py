import pytest
from httpx import AsyncClient

from app.schemas.user import UserLoginResponse, UserResponse
from tests.utils import validate_schema

pytestmark = pytest.mark.anyio

user_data = {"username": "Sovana", "email": "user@example.com", "password": "123456"}


async def test_register_success(client):
    response = await client.post("/api/v1/auth/register", json=user_data)

    assert response.status_code == 200


async def test_register_unique_exception_error(client):
    await client.post("/api/v1/auth/register", json=user_data)

    response = await client.post("/api/v1/auth/register", json=user_data)

    assert response.status_code == 409


async def test_login_success(client):
    await client.post(
        "/api/v1/auth/register",
        json=user_data,
    )
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == 200

    validate_schema(UserLoginResponse, response.json())


async def test_login_not_found_error(client):
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == 401


async def test_get_user(user_client: AsyncClient):
    response = await user_client.get("/api/v1/users/me")

    assert response.status_code == 200

    validate_schema(UserResponse, response.json())
