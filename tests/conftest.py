from typing import Iterator

import pytest

from topics.adapters.repositories.topic_repository import InMemoryTopicRepository
from topics.domain.repositories.topic_repository import TopicRepository


@pytest.fixture
def topic_repository() -> Iterator[TopicRepository]:
    yield InMemoryTopicRepository()
