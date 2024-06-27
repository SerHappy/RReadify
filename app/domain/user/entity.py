from pydantic import BaseModel


class UserDTO(BaseModel):
    """User data transfer object."""

    id: int
    email: str
    password: str
    is_verified: bool = False
    is_superuser: bool = False


class User:
    """User domain model."""

    def __init__(self, data: UserDTO) -> None:
        self.id = data.id
        self.email = data.email
        self.password = data.password
        self.is_verified = data.is_verified
        self.is_superuser = data.is_superuser
