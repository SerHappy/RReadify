import re
import uuid

from app.core.security import get_password_hash
from app.domain.user import entity, exceptions
from app.infra.uow import AbstractUnitOfWork
from app.schemas.user import UserInput


class CreateUserUseCase:
    """Responsible for creating a new user."""

    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow

    async def execute(self, user_data: UserInput) -> entity.User:
        """Creates a new user."""
        password = user_data.password
        if len(password) < entity.User.MIN_PASSWORD_LENGTH:
            raise exceptions.PasswordTooShortError
        if len(password) > entity.User.MAX_PASSWORD_LENGTH:
            raise exceptions.PasswordTooLongError
        if not re.match(entity.User.PASSWORD_PATTERN, password):
            raise exceptions.PasswordTooCommonError
        async with self._uow:
            user = await self._uow.user.get_by_email(user_data.email)
            if user:
                raise exceptions.UserAlreadyExistsError
            user = entity.User(
                entity.UserDTO(
                    id=uuid.uuid4(),
                    email=user_data.email,
                    hashed_password=get_password_hash(password),
                ),
            )
            await self._uow.user.save(user)
            await self._uow.commit()
        return user
