from fastapi import BackgroundTasks, HTTPException, status
from fastapi.routing import APIRouter

from app.api.deps import UoW
from app.domain.user import exceptions
from app.schemas.user import Message, UserInput, UserOutput
from app.services import email
from app.services.user.create import CreateUserUseCase
from app.services.user.get import GetUserUseCase
from app.services.user.verify import VerifyUserUseCase

register_router = APIRouter()


@register_router.post("/", response_model=UserOutput)
async def register(
    user_data: UserInput,
    uow: UoW,
    background_tasks: BackgroundTasks,
) -> UserOutput:
    """Registration endpoint."""
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
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists.",
        ) from None
    token = email.generate_confirmation_token(user.email)
    content = email.generate_confirmation_email(token)
    background_tasks.add_task(
        email.send_email,
        user.email,
        "Confirm your email",
        content,
    )
    return UserOutput.model_validate(user)


@register_router.post("/verify-email", response_model=Message)
async def verify_email(token: str, uow: UoW) -> Message:
    """Verify email endpoint."""
    user_email = email.verify_email_token(token)
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token.",
        )
    get_service = GetUserUseCase(uow)
    user = await get_service.get_by_email(user_email)
    verify_service = VerifyUserUseCase(uow)
    try:
        await verify_service.execute(user)
    except exceptions.UserAlreadyVerifiedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already verified.",
        ) from None
    return Message(message="Email verified.", status=status.HTTP_202_ACCEPTED)
