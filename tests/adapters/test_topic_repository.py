from typing import Iterator
from uuid import UUID

import pytest

from topics.adapters.repositories.topic_repository import (
    DatabaseSettings,
    PostgresTopicRepository,
)
from topics.domain.entities.topic import Topic
from topics.domain.errors import TopicAlreadyExistsError
from topics.domain.repositories.topic_repository import TopicRepository


class TopicRepositoryTestSuite:
    @pytest.fixture(autouse=True)
    def setup(self, topic_repository: TopicRepository) -> None:
        self.repository = topic_repository

    def test_given_existing_id_when_create_then_raises_exception(self) -> None:
        # Arrange
        topic = Topic(
            id=UUID("8623788e-3c9c-421c-ab10-92dd10405ebe"), content="Some ref"
        )
        self.repository.create(topic)

        # Act - Assert
        with pytest.raises(TopicAlreadyExistsError):
            self.repository.create(topic)


class TestInMemoryTopicRepository(TopicRepositoryTestSuite):
    ...


class TestPostgresTopicRepository(TopicRepositoryTestSuite):
    @pytest.fixture
    def topic_repository(self) -> Iterator[TopicRepository]:
        with PostgresTopicRepository(DatabaseSettings(name="test")) as repository:
            yield repository
            # Doing this here because we don't want to expose a truncate method on the repository
            if repository._db is not None:
                with repository._db.cursor() as cur:
                    cur.execute("TRUNCATE TABLE topic")
                    repository._db.commit()
