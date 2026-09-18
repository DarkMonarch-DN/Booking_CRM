from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError

from app.dependencies.services import UserServiceDep
from app.models.user import User, UserRole
from app.utils.user import decode_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
) -> int:

    try:
        payload = decode_jwt(token)

        if not payload["sub"]:
            raise HTTPException(status_code=403, detail="FORBIDDEN")

        return int(payload["sub"])

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expire token invalid.")
    except InvalidSignatureError:
        raise HTTPException(status_code=401, detail="Invalid signature token.")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


async def get_current_user(
    user_service: UserServiceDep, user_id: int = Depends(get_current_user_id)
) -> User:
    user = await user_service.find_by_id(user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


class RoleChecker:
    def __init__(self, allowed_roles: list[UserRole]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_user)) -> User:  # noqa: B008
        if user.role not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="FORBIDDEN")
        return user


allow_admin = RoleChecker([UserRole.admin])


CurrentUserIdDep = Annotated[int, Depends(get_current_user_id)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
AdminDep = Annotated[User, Depends(allow_admin)]
