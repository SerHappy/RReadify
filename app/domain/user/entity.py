from uuid import UUID

from pydantic import BaseModel


class UserDTO(BaseModel):
    """User data transfer object."""

    id: UUID
    email: str
    hashed_password: str
    is_verified: bool = False
    is_superuser: bool = False


class User:
    """User domain model."""

    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 40
    PASSWORD_PATTERN = r"((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,40})"  # noqa: S105

    def __init__(self, data: UserDTO) -> None:
        self.id = data.id
        self.email = data.email
        self.hashed_password = data.hashed_password
        self.is_verified = data.is_verified
        self.is_superuser = data.is_superuser
