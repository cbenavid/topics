import pytest

from topics.domain.entities.topic import Topic
from topics.domain.repositories.topic_repository import TopicRepository
from topics.domain.usecases.topic.create_topic import (
    CreateTopicRequest,
    CreateTopicUsecase,
)


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

    def test_given_already_created_topic_then_new_topic_has_different_id(self) -> None:
        # Arrange
        request = CreateTopicRequest(content="First topic")
        response = self.usecase.handle(request)
        first_topic_id = response.id

        request = CreateTopicRequest(content="Second topic")

        # Act
        response = self.usecase.handle(request)

        # Assert
        assert response.id != first_topic_id
