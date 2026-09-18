from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient

from app.schemas.booking import BookingResponse
from tests.api.test_items import item_data
from tests.utils import validate_schema

pytestmark = pytest.mark.anyio


booking_data = {
    "item_id": 1,
    "time_start": datetime.now().isoformat(),  # noqa: DTZ005
    "time_end": (datetime.now() + timedelta(hours=2)).isoformat(),  # noqa: DTZ005
}


async def test_get_user_bookings(user_client: AsyncClient, create_item):
    await create_item(**item_data)
    await create_item(number="43123", type="room")

    response = await user_client.get("/api/v1/bookings/my")

    assert response.status_code == 200

    validate_schema(BookingResponse, response.json())
