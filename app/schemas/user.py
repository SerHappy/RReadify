from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """User base schema."""

    model_config = ConfigDict(from_attributes=True)

    email: str


class UserInput(UserBase):
    """User input schema."""

    password: str


class UserOutput(UserBase):
    """User output schema."""

    id: int
    is_verified: bool = False
