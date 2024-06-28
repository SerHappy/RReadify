from fastapi import HTTPException, status
from fastapi.routing import APIRouter

from app.api.deps import UoW
from app.domain.user import exceptions
from app.schemas.user import UserInput, UserOutput
from app.services.user.create import CreateUserUseCase

register_router = APIRouter()


@register_router.post("/", response_model=UserOutput)
async def create_user(user_data: UserInput, uow: UoW) -> UserOutput:
    """Creates a new user."""
    service = CreateUserUseCase(uow)
    try:
        user = await service.execute(user_data)
    except exceptions.PasswordTooCommonError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too common.",
        ) from None
    except exceptions.PasswordTooLongError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too long.",
        ) from None
    except exceptions.PasswordTooShortError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is too short.",
        ) from None
    except exceptions.UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists.",
        ) from None
    return UserOutput.model_validate(user)
