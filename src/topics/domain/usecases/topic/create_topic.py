import abc
from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID

from topics.domain.entities.topic import Topic
from topics.domain.id_generator import IdGenerator
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
    id_generator: IdGenerator

    def handle(self, request: CreateTopicRequest) -> CreateTopicResponse:
        topic = Topic(id=self.id_generator.get_next(), content=request.content)
        self.topic_repository.create(topic)
        return CreateTopicResponse(id=topic.id)
