from uuid import UUID

import pytest

from topics.domain.entities.topic import Topic
from topics.domain.repositories.topic_repository import TopicRepository
from topics.domain.usecases.topic.list_topics import ListTopicsUsecase


class TestListTopicsUsecase:
    @pytest.fixture(autouse=True)
    def setup(self, topic_repository: TopicRepository) -> None:
        self.topic_repository = topic_repository
        self.usecase = ListTopicsUsecase(topic_repository=self.topic_repository)

    def test_given_no_existing_topics_then_returns_empty_list(self) -> None:
        # Act
        response = self.usecase.handle()

        # Assert
        assert response.topics == []

    def test_given_existing_topic_then_returns_list_with_topic(self) -> None:
        # Arrange
        self.topic_repository.create(
            Topic(id=UUID("8623788e-3c9c-421c-ab10-92dd10405ebe"), content="Some topic")
        )

        # Act
        response = self.usecase.handle()

        # Assert
        assert response.topics == [
            Topic(id=UUID("8623788e-3c9c-421c-ab10-92dd10405ebe"), content="Some topic")
        ]
