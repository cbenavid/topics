from uuid import UUID

import pytest

from topics.domain.entities.topic import Topic
from topics.domain.errors import TopicNotFoundError
from topics.domain.id_generator import StaticIdGenerator
from topics.domain.repositories.topic_repository import TopicRepository
from topics.domain.usecases.topic.create_topic import (
    CreateTopicRequest,
    CreateTopicUsecase,
)
from topics.domain.usecases.topic.update_topic import (
    UpdateTopicRequest,
    UpdateTopicUsecase,
)


class TestUpdateTopicUsecase:
    @pytest.fixture(autouse=True)
    def setup(self, topic_repository: TopicRepository) -> None:
        self.topic_repository = topic_repository
        self.usecase = UpdateTopicUsecase(topic_repository=self.topic_repository)

    def test_given_unexisting_id_then_raises_topic_not_found_error(self) -> None:
        # Arrange
        request = UpdateTopicRequest(
            id=UUID("98b09b66-948c-43c2-8791-5b005e40715e"), content="Updated topic"
        )

        # Act - Assert
        with pytest.raises(TopicNotFoundError):
            self.usecase.handle(request)

    def test_given_existing_id_and_new_content_then_topic_is_updated(self) -> None:
        # Arrange
        self.arrange_topic()
        request = UpdateTopicRequest(
            id=UUID("98b09b66-948c-43c2-8791-5b005e40715e"), content="Updated topic"
        )

        # Act
        self.usecase.handle(request)

        # Assert
        topic = self.topic_repository.get(request.id)
        assert topic == Topic(
            id=request.id, content="Updated topic", priority=1, discussed=False
        )

    def test_given_existing_id_and_new_discussed_then_topic_is_updated(self) -> None:
        # Arrange
        self.arrange_topic()
        request = UpdateTopicRequest(
            id=UUID("98b09b66-948c-43c2-8791-5b005e40715e"), discussed=True
        )

        # Act
        self.usecase.handle(request)

        # Assert
        topic = self.topic_repository.get(request.id)
        assert topic == Topic(
            id=request.id, content="Some topic", priority=1, discussed=True
        )

    def arrange_topic(self, content: str = "Some topic") -> None:
        usecase = CreateTopicUsecase(
            topic_repository=self.topic_repository,
            id_generator=StaticIdGenerator().with_id(
                UUID("98b09b66-948c-43c2-8791-5b005e40715e")
            ),
        )
        request = CreateTopicRequest(content=content)
        usecase.handle(request)
