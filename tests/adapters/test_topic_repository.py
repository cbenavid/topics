from typing import Iterator
from uuid import UUID

import pytest

from topics.adapters.repositories.topic_repository import (
    DatabaseSettings,
    PostgresTopicRepository,
)
from topics.domain.entities.topic import Topic
from topics.domain.errors import TopicAlreadyExistsError, TopicNotFoundError
from topics.domain.repositories.topic_repository import TopicRepository


class TopicRepositoryTestSuite:
    @pytest.fixture(autouse=True)
    def setup(self, topic_repository: TopicRepository) -> None:
        self.repository = topic_repository

    def test_given_existing_id_when_create_then_raises_exception(self) -> None:
        topic = make_topic()
        self.repository.create(topic)
        with pytest.raises(TopicAlreadyExistsError):
            self.repository.create(topic)

    def test_given_new_topic_when_create_then_can_get_by_id(self) -> None:
        topic = make_topic()
        self.repository.create(topic)
        retrieved_topic = self.repository.get(topic.id)
        assert retrieved_topic == topic

    def test_given_nonexistent_id_when_get_then_raises_exception(self) -> None:
        topic = make_topic()
        with pytest.raises(TopicNotFoundError):
            self.repository.get(topic.id)

    def test_given_no_topics_when_list_then_returns_empty_list(self) -> None:
        retrieved_topics = self.repository.list()
        assert retrieved_topics == []

    def test_given_created_topic_when_list_then_returns_list_with_topic(self) -> None:
        topic = make_topic()
        self.repository.create(topic)
        retrieved_topics = self.repository.list()
        assert retrieved_topics == [topic]


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


def make_topic() -> Topic:
    topic = Topic(id=UUID("8623788e-3c9c-421c-ab10-92dd10405ebe"), content="Some ref")
    return topic
