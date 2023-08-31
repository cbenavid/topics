from dataclasses import dataclass
from uuid import UUID

from topics.domain.entities.topic import Topic
from topics.domain.id_generator import IdGenerator
from topics.domain.repositories.topic_repository import TopicRepository
from topics.domain.usecases.base import Usecase


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
