import abc
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

from topics.domain.entities.topic import Topic
from topics.domain.repositories.topic_repository import TopicRepository

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


@dataclass(kw_only=True)
class CreateTopicUsecase(Usecase[CreateTopicRequest, CreateTopicResponse]):
    topic_repository: TopicRepository

    def handle(self, request: CreateTopicRequest) -> CreateTopicResponse:
        id_ = UUID("8623788e-3c9c-421c-ab10-92dd10405ebe")
        topic = Topic(id=id_, content=request.content)
        self.topic_repository.create(topic)
        return CreateTopicResponse(id=id_)
