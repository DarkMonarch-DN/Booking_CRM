from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, field_validator

from app.schemas.item import ItemResponse


class BookingCreate(BaseModel):
    item_id: int

    time_start: datetime
    time_end: datetime

    @field_validator("time_start", "time_end", mode="before")
    @classmethod
    def convert_and_force_utc(cls, v):
        if isinstance(v, str):
            try:
                v = datetime.fromisoformat(v)
            except ValueError:
                return v

        if isinstance(v, datetime):
            if v.tzinfo is None:
                return v.replace(tzinfo=timezone.utc)  # noqa: UP017
            return v.astimezone(timezone.utc)  # noqa: UP017

        return v

    @field_validator("time_start", "time_end", mode="after")
    @classmethod
    def validate_time(cls, v):
        now = datetime.now(tz=timezone.utc) + timedelta(minutes=10)  # noqa: UP017
        if v < now:
            raise ValueError(
                "The start time and the start time cannot be the current time"
            )
        return v


class BookingResponse(BaseModel):
    id: int

    user_id: int
    item_id: int

    time_start: datetime
    time_end: datetime

    item: ItemResponse | None = None

    created_at: datetime
