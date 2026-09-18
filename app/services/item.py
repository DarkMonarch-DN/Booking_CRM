from typing import Sequence  # noqa: UP035

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate


class ItemService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_new_item(self, item_in: ItemCreate):
        item = Item(**item_in.model_dump(exclude_unset=True))

        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def find_all(self) -> Sequence[Item]:
        res = await self.session.execute(select(Item))
        return res.scalars().all()

    async def delete(self, item_id: int) -> Item:
        existing = await self.session.get(Item, item_id)

        if not existing:
            raise HTTPException(status_code=404, detail="Item not found")

        await self.session.delete(existing)
        await self.session.commit()

        return existing
