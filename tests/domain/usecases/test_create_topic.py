from uuid import UUID

import pytest

from topics.domain.entities.topic import Topic
from topics.domain.id_generator import StaticIdGenerator
from topics.domain.repositories.topic_repository import TopicRepository
from topics.domain.usecases.topic.create_topic import (
    CreateTopicRequest,
    CreateTopicUsecase,
)


class TestCreateTopicUsecase:
    @pytest.fixture(autouse=True)
    def setup(self, topic_repository: TopicRepository) -> None:
        self.topic_repository = topic_repository
        self.id_generator = StaticIdGenerator().with_id(
            UUID("8623788e-3c9c-421c-ab10-92dd10405ebe")
        )
        self.usecase = CreateTopicUsecase(
            topic_repository=self.topic_repository, id_generator=self.id_generator
        )

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

    def test_given_already_created_topic_then_new_topic_can_be_created(self) -> None:
        # Arrange
        self.arrange_topic("First topic")
        self.id_generator.with_id(UUID("98b09b66-948c-43c2-8791-5b005e40715e"))
        request = CreateTopicRequest(content="Second topic")

        # Act
        response = self.usecase.handle(request)

        # Assert
        expected_topic = Topic(
            id=response.id, content="Second topic", priority=1, discussed=False
        )
        self.assert_topic_in_repository(expected_topic)

    def arrange_topic(self, content: str) -> None:
        request = CreateTopicRequest(content=content)
        self.usecase.handle(request)

    def assert_topic_in_repository(self, expected_topic: Topic) -> None:
        topic = self.topic_repository.get(expected_topic.id)
        assert topic == expected_topic
