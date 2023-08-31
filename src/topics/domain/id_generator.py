import abc
from uuid import UUID, uuid4

from typing_extensions import Self


class IdGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_next(self) -> UUID:
        ...


class RandomIdGenerator(IdGenerator):
    def get_next(self) -> UUID:
        return uuid4()


class StaticIdGenerator(IdGenerator):
    def __init__(self) -> None:
        self._id: UUID | None = None

    def with_id(self, id: UUID) -> Self:
        self._id = id
        return self

    def get_next(self) -> UUID:
        if self._id is None:
            raise ValueError("id has not been set yet")
        return self._id
