from typing import Annotated
from uuid import UUID

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
)


class UserBase(BaseModel):
    """User base schema."""

    model_config = ConfigDict(from_attributes=True)

    email: EmailStr


def validate_password(value: str):
    min_length = 8
    max_length = 40
    if len(value) < min_length:
        message = f"Password must have at least {min_length} characters."
    if len(value) > max_length:
        message = f"Password must have at most {max_length} characters."
    


class UserInput(UserBase):
    """User input schema."""

    password: Annotated[str, AfterValidator(validate_password)]


class UserOutput(UserBase):
    """User output schema."""

    id: UUID
    is_verified: bool = False
