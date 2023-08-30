from typing import Iterator

import pytest

from topics.adapters.repositories.topic_repository import InMemoryTopicRepository
from topics.domain.entities.topic import Topic
from topics.domain.repositories.topic_repository import TopicRepository
from topics.domain.usecases.topic.create_topic import (
    CreateTopicRequest,
    CreateTopicUsecase,
)


@pytest.fixture
def topic_repository() -> Iterator[TopicRepository]:
    yield InMemoryTopicRepository()


class TestCreateTopicUsecase:
    @pytest.fixture(autouse=True)
    def setup(self, topic_repository: TopicRepository) -> None:
        self.topic_repository = topic_repository
        self.usecase = CreateTopicUsecase(topic_repository=self.topic_repository)

    @pytest.mark.parametrize("content", ["First topic", "Second topic"])
    def test_given_content_then_topic_is_created(self, content: str) -> None:
        # Arrange
        request = CreateTopicRequest(content=content)

        # Act
        response = self.usecase.handle(request)

        # Assert
        topic = self.topic_repository.get(response.id)
        assert topic == Topic(
            id=response.id, content=content, priority=1, discussed=False
        )
