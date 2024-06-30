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


class EmailSettings(BaseModel):
    """Email settings."""

    FROM_EMAIL: str
    TEST_USER: str | None = None
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str


class SecuritySettings(BaseModel):
    """Security settings."""

    DOMAIN: str = "http://localhost:8000"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 3600  # 1 hour
    EMAIL_CONFIRMATION_EXPIRE: int = 600  # 10 minutes
    EMAIL_TOKEN_TYPE: str = "email_confirmation"
    EMAIL_CONFIRM_URL: str = DOMAIN + "/register/verify-email"


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
    EMAIL: EmailSettings
    SECURITY: SecuritySettings


settings = Settings()  # type: ignore[reportCallIssue]
