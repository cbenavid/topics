from collections.abc import Iterator
from typing import Any
from uuid import UUID

import pytest
from flask import Flask
from flask.testing import FlaskClient

from topics.app import create_app
from topics.domain.usecases.base import Usecase
from topics.domain.usecases.topic.create_topic import (
    CreateTopicRequest,
    CreateTopicResponse,
)
from topics.domain.usecases.topic.list_topics import ListTopicsResponse


@pytest.fixture
def list_topics_usecase() -> Usecase[None, ListTopicsResponse]:
    return SpyListTopicsUsecase()


@pytest.fixture
def create_topic_usecase() -> Usecase[CreateTopicRequest, CreateTopicResponse]:
    return SpyCreateTopicUsecase()


@pytest.fixture
def app(
    list_topics_usecase: Usecase[None, ListTopicsResponse],
    create_topic_usecase: Usecase[CreateTopicRequest, CreateTopicResponse],
) -> Iterator[Flask]:
    app = create_app(
        list_topics_usecase=list_topics_usecase,
        create_topic_usecase=create_topic_usecase,
    )
    app.config.update({"TESTING": True})
    yield app


class SpyListTopicsUsecase(Usecase[None, ListTopicsResponse]):
    def __init__(self) -> None:
        self._called = False

    @property
    def called(self) -> bool:
        return self._called

    def handle(self, request: None = None) -> ListTopicsResponse:
        self._called = True
        return ListTopicsResponse(topics=[])


class SpyCreateTopicUsecase(Usecase[CreateTopicRequest, CreateTopicResponse]):
    def __init__(self) -> None:
        self._called = False

    @property
    def called(self) -> bool:
        return self._called

    def handle(self, request: CreateTopicRequest) -> CreateTopicResponse:
        self._called = True
        return CreateTopicResponse(id=UUID("8623788e-3c9c-421c-ab10-92dd10405ebe"))


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


def test_get_topics_route_calls_usecase(
    client: FlaskClient, list_topics_usecase: SpyListTopicsUsecase
) -> None:
    response = client.get("/topics")
    assert response.status_code == 200
    assert response.json == []
    assert list_topics_usecase.called


def test_create_topic_route_calls_usecase(
    client: FlaskClient, create_topic_usecase: SpyCreateTopicUsecase
) -> None:
    response = client.post("/topics", json={"content": "Some topic to discuss"})
    assert response.status_code == 200
    assert response.json == {"id": "8623788e-3c9c-421c-ab10-92dd10405ebe"}
    assert create_topic_usecase.called


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"content": {"foo": "bar"}},
        {"content": "Some content", "foo": "bar"},
    ],
)
def test_create_topic_route_returns_422_if_payload_is_incorrect(
    client: FlaskClient, payload: dict[str, Any]
) -> None:
    response = client.post("/topics", json=payload)
    assert response.status_code == 422
