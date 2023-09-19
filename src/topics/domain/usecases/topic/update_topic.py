from dataclasses import dataclass, replace
from typing import Any
from uuid import UUID

from topics.domain.repositories.topic_repository import TopicRepository
from topics.domain.usecases.base import Usecase


@dataclass(kw_only=True)
class UpdateTopicRequest:
    id: UUID
    content: str | None = None
    discussed: bool | None = None


@dataclass(kw_only=True)
class UpdateTopicUsecase(Usecase[UpdateTopicRequest, None]):
    topic_repository: TopicRepository

    def handle(self, request: UpdateTopicRequest) -> None:
        topic = self.topic_repository.get(request.id)
        updated_fields: dict[str, Any] = {}
        if request.content is not None:
            updated_fields["content"] = request.content
        if request.discussed is not None:
            updated_fields["discussed"] = request.discussed
        self.topic_repository.update(replace(topic, **updated_fields))
