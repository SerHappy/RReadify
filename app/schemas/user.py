from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
)


class UserBase(BaseModel):
    """User base schema."""

    model_config = ConfigDict(from_attributes=True)

    email: EmailStr


class UserInput(UserBase):
    """User input schema."""

    password: str


class UserOutput(UserBase):
    """User output schema."""

    id: UUID
    is_verified: bool = False


class Message(BaseModel):
    """Message schema."""

    message: str
    status: int
