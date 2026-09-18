from datetime import datetime

from pydantic import BaseModel

from app.models.item import ItemStatus, ItemType


class ItemCreate(BaseModel):
    number: str
    type: ItemType = ItemType.room
    status: ItemStatus | None = None


class ItemResponse(BaseModel):
    id: int
    number: str
    type: ItemType
    status: ItemStatus
    created_at: datetime
