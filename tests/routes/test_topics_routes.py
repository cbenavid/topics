from collections.abc import Iterator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from topics.app import create_app
from topics.domain.usecases.base import Usecase
from topics.domain.usecases.topic.list_topics import ListTopicsResponse


@pytest.fixture
def list_topics_usecase() -> Usecase[None, ListTopicsResponse]:
    return SpyListTopicsUsecase()


@pytest.fixture
def app(list_topics_usecase: Usecase[None, ListTopicsResponse]) -> Iterator[Flask]:
    app = create_app(list_topics_usecase=list_topics_usecase)
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


class SpyListTopicsUsecase(Usecase[None, ListTopicsResponse]):
    def __init__(self) -> None:
        self._called = False

    @property
    def called(self) -> bool:
        return self._called

    def handle(self, request: None = None) -> ListTopicsResponse:
        self._called = True
        return ListTopicsResponse(topics=[])


def test_get_topics_route_calls_usecase(
    client: FlaskClient, list_topics_usecase: SpyListTopicsUsecase
) -> None:
    response = client.get("/topics")
    assert response.status_code == 200
    assert response.json == []
    assert list_topics_usecase.called
