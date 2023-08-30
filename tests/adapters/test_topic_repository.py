from uuid import UUID

import pytest

from topics.domain.entities.topic import Topic
from topics.domain.errors import TopicAlreadyExistsError
from topics.domain.repositories.topic_repository import TopicRepository


class TestInMemoryTopicRepository:
    @pytest.fixture(autouse=True)
    def setup(self, topic_repository: TopicRepository) -> None:
        self.topic_repository = topic_repository

    def test_given_existing_id_when_create_then_raises_exception(self) -> None:
        # Arrange
        topic = Topic(
            id=UUID("8623788e-3c9c-421c-ab10-92dd10405ebe"), content="Some ref"
        )
        self.topic_repository.create(topic)

        # Act - Assert
        with pytest.raises(TopicAlreadyExistsError):
            self.topic_repository.create(topic)
