from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.bookings import router as booking_router
from app.api.v1.items import router as item_router
from app.api.v1.users import router as users_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(item_router, prefix="/items", tags=["Items"])
router.include_router(booking_router, prefix="/bookings", tags=["Bookings"])
