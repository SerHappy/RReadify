from abc import ABC, abstractmethod
from app.models.user import UserORM

class AbstractUserRepository(ABC):
    """Interface for User Repository."""

    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserORM:
        pass

    @abstractmethod
    def get_users(self) -> list[UserORM]:
        pass

    @abstractmethod
    def create_user(self, user) -> UserORM:
        pass

    @abstractmethod
    def update_user(self, user) -> UserORM:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        pass
