from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    """Postgres settings."""

    SERVER: str
    PORT: int
    USER: str
    PASSWORD: str
    DB: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:  # noqa: N802
        """Create a SQLAlchemy database URI."""
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.USER,
            password=self.PASSWORD,
            host=self.SERVER,
            port=self.PORT,
            path=self.DB,
        )


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        env_nested_delimiter="__",
        frozen=True,
    )
    POSTGRES: PostgresSettings


settings = Settings()  # type: ignore[reportCallIssue]
