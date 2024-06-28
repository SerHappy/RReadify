from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.user import exceptions
from app.domain.user.entity import User


class AbstractUserRepository(ABC):
    """Interface for User Repository."""

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User:
        """Get a user by its ID."""

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        """Get a user by its email."""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Saves a user."""

    @abstractmethod
    async def delete(self, user: User) -> None:
        """Delete a user."""


class UserRepository(AbstractUserRepository):
    """User Repository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> User:
        """Get a user by its ID."""
        try:
            return await self._session.get_one(User, user_id)
        except NoResultFound as e:
            raise exceptions.UserNotFoundError from e

    async def get_by_email(self, email: str) -> User | None:
        """Get a user by its email."""
        return (
            await self._session.execute(
                select(User).filter_by(email=email),
            )
        ).scalar_one_or_none()

    async def save(self, user: User) -> User:
        """Saves a user into the database."""
        self._session.add(user)
        return user

    async def delete(self, user: User) -> None:
        """Delete a user."""
        await self._session.delete(user)
