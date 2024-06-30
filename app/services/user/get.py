from app.domain.user import entity, exceptions
from app.infra.uow import AbstractUnitOfWork


class GetUserUseCase:
    """Responsible for getting a user."""

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def get_by_email(self, email: str) -> entity.User:
        """Get a user by email."""
        async with self._uow:
            user = await self._uow.user.get_by_email(email)
            if not user:
                raise exceptions.UserNotFoundError
            await self._uow.commit()
        return user
