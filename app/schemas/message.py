from pydantic import BaseModel


class Message(BaseModel):
    """Message schema."""

    message: str
    status: int
