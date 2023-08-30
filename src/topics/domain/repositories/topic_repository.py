import abc
from uuid import UUID

from topics.domain.entities.topic import Topic


class TopicRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get(self, id: UUID) -> Topic:
        ...
