from uuid import UUID

from topics.domain.entities.topic import Topic
from topics.domain.errors import TopicAlreadyExistsError
from topics.domain.repositories.topic_repository import TopicRepository


class InMemoryTopicRepository(TopicRepository):
    def __init__(self) -> None:
        self._topics: dict[UUID, Topic] = {}

    def get(self, id: UUID) -> Topic:
        return self._topics[id]

    def create(self, topic: Topic) -> None:
        if topic.id in self._topics:
            raise TopicAlreadyExistsError
        self._topics[topic.id] = topic
