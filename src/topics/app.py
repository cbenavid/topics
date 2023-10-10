from dataclasses import asdict
from typing import Any

from flask import Flask, request
from marshmallow import Schema, ValidationError, fields

from topics.adapters.repositories.topic_repository import InMemoryTopicRepository
from topics.domain.entities.topic import Topic
from topics.domain.id_generator import RandomIdGenerator
from topics.domain.usecases.base import Usecase
from topics.domain.usecases.topic.create_topic import (
    CreateTopicRequest,
    CreateTopicResponse,
    CreateTopicUsecase,
)
from topics.domain.usecases.topic.list_topics import (
    ListTopicsResponse,
    ListTopicsUsecase,
)


class CreateTopicRequestSchema(Schema):
    content = fields.Str(required=True)


def create_app(
    list_topics_usecase: Usecase[None, ListTopicsResponse],
    create_topic_usecase: Usecase[CreateTopicRequest, CreateTopicResponse],
) -> Flask:
    app = Flask(__name__)

    @app.get("/topics")
    def get_topics() -> list[Topic]:
        response = list_topics_usecase.handle(None)
        return response.topics

    @app.post("/topics")
    def create_topic() -> tuple[dict[str, Any], int]:
        schema = CreateTopicRequestSchema()
        request_json = request.get_json()
        try:
            validated_payload = schema.load(request_json, unknown="raise")
        except ValidationError:
            return {}, 422
        create_request = CreateTopicRequest(**validated_payload)
        response = create_topic_usecase.handle(create_request)
        return asdict(response), 200

    return app


topic_repository = InMemoryTopicRepository()
id_generator = RandomIdGenerator()
list_topics_usecase = ListTopicsUsecase(topic_repository=topic_repository)
create_topic_usecase = CreateTopicUsecase(
    topic_repository=topic_repository, id_generator=id_generator
)
app = create_app(list_topics_usecase, create_topic_usecase)
