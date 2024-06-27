from app.infra.uow import AbstractUnitOfWork


class CreateUserUseCase:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self._uow = uow
