from dataclasses import dataclass

from topics.domain.entities.topic import Topic
from topics.domain.repositories.topic_repository import TopicRepository
from topics.domain.usecases.base import Usecase


@dataclass
class ListTopicsResponse:
    topics: list[Topic]


@dataclass(kw_only=True)
class ListTopicsUsecase(Usecase[None, ListTopicsResponse]):
    topic_repository: TopicRepository

    def handle(self, request: None = None) -> ListTopicsResponse:
        topics = self.topic_repository.list()
        return ListTopicsResponse(topics=topics)
