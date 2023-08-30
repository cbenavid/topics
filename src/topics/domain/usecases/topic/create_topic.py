import abc
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT")


class Usecase(Generic[RequestT, ResponseT], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def handle(self, request: RequestT) -> ResponseT:
        ...


@dataclass
class CreateTopicRequest:
    content: str


@dataclass
class CreateTopicResponse:
    id: UUID


@dataclass
class CreateTopicUsecase(Usecase[CreateTopicRequest, CreateTopicResponse]):
    def handle(self, request: CreateTopicRequest) -> CreateTopicResponse:
        return CreateTopicResponse(id=UUID("8623788e-3c9c-421c-ab10-92dd10405ebe"))
