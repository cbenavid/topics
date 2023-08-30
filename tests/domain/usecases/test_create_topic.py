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
    def test_given_content_then_topic_is_created(
        self, topic_repository: TopicRepository
    ) -> None:
        # Arrange
        usecase = CreateTopicUsecase()
        request = CreateTopicRequest(content="Some ref")

        # Act
        response = usecase.handle(request)

        # Assert
        topic = topic_repository.get(response.id)
        assert topic == Topic(
            id=response.id, content="Some ref", priority=1, discussed=False
        )
