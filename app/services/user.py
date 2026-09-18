from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.user import check_password, encode_jwt, hash_password


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def register_new_user(self, user_in: UserCreate) -> dict:
        existing = await self.find_by_email(user_in.email)

        if existing:
            raise HTTPException(
                status_code=409, detail="The user already has been registered"
            )

        user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=hash_password(user_in.password),
        )
        self.session.add(user)
        await self.session.commit()

        return {"success": True, "message": "Registration was successful"}

    async def login(self, user_in: OAuth2PasswordRequestForm) -> tuple[User, str]:
        unauth_exception = HTTPException(
            status_code=401,
            detail="Incorrect login or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = await self.find_by_email(user_in.username)

        if not user:
            raise unauth_exception
        if not check_password(user_in.password, user.hashed_password):
            raise unauth_exception

        access_token = encode_jwt(
            {"sub": str(user.id), "username": user.username, "role": user.role}
        )

        return user, access_token

    async def find_by_id(self, user_id) -> User | None:
        return await self.session.get(User, user_id)

    async def find_by_email(self, email: str) -> User | None:
        res = await self.session.execute(select(User).where(User.email == email))
        return res.scalar_one_or_none()
