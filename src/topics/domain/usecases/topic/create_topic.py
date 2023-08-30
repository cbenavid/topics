import abc
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID, uuid4

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
        topic = Topic(id=generate_id(), content=request.content)
        self.topic_repository.create(topic)
        return CreateTopicResponse(id=topic.id)


def generate_id() -> UUID:
    return uuid4()
