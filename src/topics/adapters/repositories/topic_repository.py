from uuid import UUID

from topics.domain.entities.topic import Topic
from topics.domain.repositories.topic_repository import TopicRepository


class InMemoryTopicRepository(TopicRepository):
    def get(self, id: UUID) -> Topic:
        return Topic(id=id, content="Some ref")
