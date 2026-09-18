from typing import Sequence  # noqa: UP035

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.booking import Booking
from app.models.item import Item
from app.schemas.booking import BookingCreate


class BookingService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_all(self):
        res = await self.session.execute(select(Booking))

        return res.scalars().all()

    async def find_all_by_user(self, user_id: int) -> Sequence[Booking]:
        res = await self.session.execute(
            select(Booking)
            .where(Booking.user_id == user_id)
            .options(selectinload(Booking.item))
        )

        return res.scalars().all()

    async def create(self, booking_in: BookingCreate, user_id: int):
        existing_item = await self.session.get(Item, booking_in.item_id)

        if not existing_item:
            raise HTTPException(status_code=404, detail="Room or table not found")

        query = await self.session.execute(
            select(Booking).where(
                and_(
                    Booking.item_id == booking_in.item_id,
                    booking_in.time_start < Booking.time_end,
                    booking_in.time_end > Booking.time_start,
                )
            )
        )
        existing = query.first()

        if existing:
            raise HTTPException(
                status_code=400, detail="The table or room is occupied at this time."
            )

        booking = Booking(**booking_in.model_dump(), user_id=user_id)
        self.session.add(booking)
        await self.session.commit()
        await self.session.refresh(booking)
        return booking

    async def cancel_booking(self, booking_id: int, user_id: int):
        query = await self.session.execute(
            select(Booking)
            .where(Booking.id == booking_id)
            .where(Booking.user_id == user_id)
        )
        existing = query.scalar_one_or_none()
        if not existing:
            raise HTTPException(
                status_code=400,
                detail="This item does not belong to you, or it does not exist",
            )

        await self.session.delete(existing)
        await self.session.commit()

        return existing
