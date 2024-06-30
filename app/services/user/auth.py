from app.core.security import verify_password
from app.domain.user import entity, exceptions
from app.infra.uow import AbstractUnitOfWork


class AuthenticateUserUseCase:
    """Responsible for authenticating a user."""

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def execute(self, user: entity.User, password: str) -> entity.User:
        """Authenticates a user."""
        async with self._uow:
            if not verify_password(
                plain_password=password,
                hashed_password=user.hashed_password,
            ):
                raise exceptions.InvalidCredentialsError
            if not user.is_verified:
                raise exceptions.UserNotVerifiedError
            return user
