from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.booking import Booking


class ItemType(str, Enum):
    room = "room"
    table = "table"


class ItemStatus(str, Enum):
    active = "active"
    repair = "repair"


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)

    number: Mapped[str] = mapped_column(unique=True)
    type: Mapped[ItemType]
    status: Mapped[ItemStatus] = mapped_column(default=ItemStatus.active)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="item")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
