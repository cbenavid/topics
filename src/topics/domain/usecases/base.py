import abc
from typing import Generic, TypeVar

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class Usecase(Generic[RequestT, ResponseT], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, request: RequestT) -> ResponseT:
        ...
