from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_db_session
from app.services.booking import BookingService
from app.services.item import ItemService
from app.services.user import UserService


async def get_user_service(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return UserService(session)


async def get_item_service(session: Annotated[AsyncSession, Depends(get_db_session)]):
    return ItemService(session)


async def get_booking_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    return BookingService(session)


# Aliases
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]
BookingServiceDep = Annotated[BookingService, Depends(get_booking_service)]
