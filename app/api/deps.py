from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.infra.uow import SQLALchemyUnitOfWork

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.SECURITY.DOMAIN}/auth/access-token",
)
optional_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.SECURITY.DOMAIN}/auth/access-token",
    auto_error=False,
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]
OptionalTokenDep = Annotated[str | None, Depends(optional_oauth2)]


async def get_uow() -> AsyncGenerator[SQLALchemyUnitOfWork, None]:
    """Dependency to get the unit of work instance."""
    uow = SQLALchemyUnitOfWork()
    yield uow


UoW = Annotated[SQLALchemyUnitOfWork, Depends(get_uow)]
