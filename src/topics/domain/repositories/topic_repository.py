import abc
from uuid import UUID

from topics.domain.entities.topic import Topic


class TopicRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, id: UUID) -> Topic:
        ...

    @abc.abstractmethod
    def create(self, topic: Topic) -> None:
        ...

    @abc.abstractmethod
    def update(self, topic: Topic) -> None:
        ...

    @abc.abstractmethod
    def list(self) -> list[Topic]:
        ...
