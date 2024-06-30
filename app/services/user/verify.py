from app.domain.user import entity, exceptions
from app.infra.uow import AbstractUnitOfWork


class VerifyUserUseCase:
    """Responsible for verifying a user."""

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def execute(self, user: entity.User) -> entity.User:
        """Get a user by email."""
        async with self._uow:
            if user.is_verified:
                raise exceptions.UserAlreadyVerifiedError
            user.is_verified = True
            user = await self._uow.user.save(user)
            await self._uow.commit()
            return user
