from datetime import timedelta
from typing import Annotated

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import UoW
from app.core.config import settings
from app.core.security import create_access_token
from app.domain.user import exceptions
from app.schemas.token import AccessToken
from app.services.user.auth import AuthenticateUserUseCase
from app.services.user.get import GetUserUseCase

auth_router = APIRouter()


@auth_router.post("/access-token")
async def login_via_access_token(
    uow: UoW,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AccessToken:
    """Login endpoint."""
    get_service = GetUserUseCase(uow)
    try:
        user = await get_service.get_by_email(email=form_data.username)
    except exceptions.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from None
    auth_service = AuthenticateUserUseCase(uow)
    try:
        await auth_service.execute(
            user=user,
            password=form_data.password,
        )
    except exceptions.InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        ) from None
    except exceptions.UserNotVerifiedError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not verified",
        ) from None
    return AccessToken(
        access_token=create_access_token(
            {"sub": str(user.id)},
            expires_delta=timedelta(seconds=settings.SECURITY.ACCESS_TOKEN_EXPIRE),
        ),
    )
