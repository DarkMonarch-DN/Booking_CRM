import pytest
from httpx import AsyncClient

from app.schemas.item import ItemResponse
from tests.utils import validate_schema

pytestmark = pytest.mark.anyio


item_data = {"number": "123456", "type": "room"}


async def test_get_items_empty(client: AsyncClient):
    response = await client.get("/api/v1/items/")

    assert response.status_code == 200

    validate_schema(ItemResponse, response.json())


async def test_create_item(user_client: AsyncClient):
    response = await user_client.post("/api/v1/items/", json=item_data)

    assert response.status_code == 403
