from flask import Flask

from topics.adapters.repositories.topic_repository import InMemoryTopicRepository
from topics.domain.entities.topic import Topic
from topics.domain.usecases.base import Usecase
from topics.domain.usecases.topic.list_topics import (
    ListTopicsResponse,
    ListTopicsUsecase,
)


def create_app(list_topics_usecase: Usecase[None, ListTopicsResponse]) -> Flask:
    app = Flask(__name__)

    @app.get("/topics")
    def get_topics() -> list[Topic]:
        response = list_topics_usecase.handle()
        return response.topics

    return app


topic_repository = InMemoryTopicRepository()
list_topics_usecase = ListTopicsUsecase(topic_repository=topic_repository)
app = create_app(list_topics_usecase)
