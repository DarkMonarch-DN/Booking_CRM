from fastapi import APIRouter

from app.dependencies.auth import AdminDep, CurrentUserIdDep
from app.dependencies.services import BookingServiceDep
from app.schemas.booking import BookingCreate, BookingResponse

router = APIRouter()


# Admin
@router.get("/", response_model=list[BookingResponse])
async def get_all(booking_service: BookingServiceDep, current_user: AdminDep):
    return await booking_service.find_all()


@router.get("/my", response_model=list[BookingResponse])
async def get_all_by_user(
    booking_service: BookingServiceDep, current_user_id: CurrentUserIdDep
):
    return await booking_service.find_all_by_user(current_user_id)


@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking_in: BookingCreate,
    booking_service: BookingServiceDep,
    current_user_id: CurrentUserIdDep,
):
    return await booking_service.create(booking_in, current_user_id)


@router.delete("/{booking_id}", response_model=BookingResponse)
async def cancel_booking(
    booking_id: int,
    booking_service: BookingServiceDep,
    current_user_id: CurrentUserIdDep,
):
    return await booking_service.cancel_booking(booking_id, current_user_id)
