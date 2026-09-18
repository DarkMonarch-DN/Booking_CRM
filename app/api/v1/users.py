from fastapi import APIRouter

from app.dependencies.auth import CurrentUserDep
from app.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: CurrentUserDep):
    return current_user
