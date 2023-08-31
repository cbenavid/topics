from dataclasses import dataclass
from uuid import UUID

from topics.domain.errors import TopicNotFoundError
from topics.domain.usecases.base import Usecase


@dataclass(kw_only=True)
class UpdateTopicRequest:
    id: UUID


@dataclass(kw_only=True)
class UpdateTopicUsecase(Usecase[UpdateTopicRequest, None]):
    def handle(self, request: UpdateTopicRequest) -> None:
        raise TopicNotFoundError
