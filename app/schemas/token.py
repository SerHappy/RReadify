from pydantic import BaseModel


class AccessToken(BaseModel):
    """Access token schema."""

    access_token: str
    token_type: str = "bearer"


class AccessTokenPayload(BaseModel):
    """Access token payload schema."""

    sub: str | None = None
