from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from app.infra.uow import SQLALchemyUnitOfWork


async def get_uow() -> AsyncGenerator[SQLALchemyUnitOfWork, None]:
    """Dependency to get the unit of work instance."""
    uow = SQLALchemyUnitOfWork()
    yield uow


UoW = Annotated[SQLALchemyUnitOfWork, Depends(get_uow)]
