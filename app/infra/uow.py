import abc
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.infra.repositories.user import AbstractUserRepository, UserRepository

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    create_async_engine(
        str(settings.POSTGRES.SQLALCHEMY_DATABASE_URI),
        echo=True,
    ),
    expire_on_commit=False,
)


class AbstractUnitOfWork(abc.ABC):
    """
    An abstract unit of work interface.

    All unit of work classes should implement this interface.
    """

    user: AbstractUserRepository

    async def __aenter__(self) -> Self:
        """
        Enters the unit of work context manager.

        Typically, this method is used to initialize session, repositories, etc.
        Returns self to allow chaining.
        """
        return self

    async def __aexit__(self, *args) -> None:
        """
        Exits the unit of work context manager.

        Used rollback all non-committed changes, close the session, etc.
        """
        await self.rollback()

    async def commit(self) -> None:
        """
        Commits all changes to the database.

        This is an API to _commit method,
        which should be implemented by the concrete unit of work class.
        """
        await self._commit()

    @abc.abstractmethod
    async def _commit(self) -> None:
        """
        Implementation of the commit method.

        Should be implemented by the concrete unit of work class.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self) -> None:
        """
        Rolls back all non-committed changes.

        Should be implemented by the concrete unit of work class.
        """
        raise NotImplementedError


class SQLALchemyUnitOfWork(AbstractUnitOfWork):
    """
    SQLAlchemy unit of work implementation.

    It interacts with the database using SQLAlchemy.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] = session_factory,
    ) -> None:
        """
        Initializes the unit of work instance.

        Uses the provided session factory.
        """
        self.session_factory = session_factory

    async def __aenter__(self) -> Self:
        """Initializes the session and repositories."""
        self.session = self.session_factory()
        self.user = UserRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args) -> None:
        """Rolls back all changes and closes the session."""
        await super().__aexit__(*args)
        await self.session.close()

    async def _commit(self) -> None:
        """Saves all changes to the database."""
        await self.session.commit()

    async def rollback(self) -> None:
        """Rolls back all changes."""
        await self.session.rollback()
