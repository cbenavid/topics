from uuid import UUID

from topics.domain.entities.topic import Topic
from topics.domain.errors import TopicAlreadyExistsError, TopicNotFoundError
from topics.domain.repositories.topic_repository import TopicRepository


class InMemoryTopicRepository(TopicRepository):
    def __init__(self) -> None:
        self._topics: dict[UUID, Topic] = {}

    def get(self, id: UUID) -> Topic:
        try:
            return self._topics[id]
        except KeyError:
            raise TopicNotFoundError

    def create(self, topic: Topic) -> None:
        if topic.id in self._topics:
            raise TopicAlreadyExistsError
        self._topics[topic.id] = topic

    def update(self, topic: Topic) -> None:
        if topic.id not in self._topics:
            raise TopicNotFoundError
        self._topics[topic.id] = topic
