import abc
from typing import Generic, TypeVar, overload

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class Usecase(Generic[RequestT, ResponseT], metaclass=abc.ABCMeta):
    @overload
    def handle(self, request: RequestT) -> ResponseT:
        ...

    @overload
    def handle(self, request: None = None) -> ResponseT:
        ...

    @abc.abstractmethod
    def handle(self, request: RequestT | None = None) -> ResponseT:
        ...
