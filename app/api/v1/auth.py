from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.services import UserServiceDep
from app.schemas.user import UserCreate, UserLoginResponse

router = APIRouter()


@router.post("/login", response_model=UserLoginResponse)
async def login(
    user_service: UserServiceDep,
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
):
    user, access_token = await user_service.login(form_data)

    return UserLoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,  # type: ignore
    )


@router.post("/register", response_model=None)
async def create_user(user_in: UserCreate, user_service: UserServiceDep):
    return await user_service.register_new_user(user_in)
