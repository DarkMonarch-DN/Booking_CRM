from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.booking import Booking


class UserRole(str, Enum):
    """User roles enum"""

    admin = "admin"
    regular = "regular"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(default=UserRole.regular)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
