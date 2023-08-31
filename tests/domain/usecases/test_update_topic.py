from uuid import UUID

import pytest

from topics.domain.errors import TopicNotFoundError
from topics.domain.usecases.topic.update_topic import (
    UpdateTopicRequest,
    UpdateTopicUsecase,
)


class TestUpdateTopicUsecase:
    @pytest.fixture(autouse=True)
    def setup(self) -> None:
        self.usecase = UpdateTopicUsecase()

    def test_given_unexisting_id_then_raises_topic_not_found_error(self) -> None:
        # Arrange
        request = UpdateTopicRequest(id=UUID("98b09b66-948c-43c2-8791-5b005e40715e"))

        # Act - Assert
        with pytest.raises(TopicNotFoundError):
            self.usecase.handle(request)
