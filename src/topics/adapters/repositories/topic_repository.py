import contextlib
from collections.abc import Iterator
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Self
from uuid import UUID

import psycopg
from psycopg.rows import dict_row

from topics.domain.entities.topic import Topic
from topics.domain.errors import TopicAlreadyExistsError, TopicNotFoundError
from topics.domain.repositories.topic_repository import TopicRepository


class InMemoryTopicRepository(TopicRepository):
    def __init__(self) -> None:
        self._topics: dict[UUID, Topic] = {}

    def get(self, id: UUID) -> Topic:
        try:
            return self._topics[id]
        except KeyError:
            raise TopicNotFoundError

    def create(self, topic: Topic) -> None:
        if topic.id in self._topics:
            raise TopicAlreadyExistsError
        self._topics[topic.id] = topic

    def update(self, topic: Topic) -> None:
        if topic.id not in self._topics:
            raise TopicNotFoundError
        self._topics[topic.id] = topic

    def list(self) -> list[Topic]:
        return [topic for topic in self._topics.values()]


@dataclass(kw_only=True)
class DatabaseSettings:
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    name: str


class PostgresTopicRepository(TopicRepository):
    def __init__(self, settings: DatabaseSettings):
        self._settings = settings
        self._db: psycopg.connection.Connection[dict[str, Any]] | None = None

    def __enter__(self) -> Self:
        return self.open()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    @contextlib.contextmanager
    def _get_cursor(
        self,
    ) -> Iterator[
        psycopg.Cursor[dict[str, Any]] | psycopg.ServerCursor[dict[str, Any]]
    ]:
        if self._db is None:
            raise ValueError("Database connection has not yet been opened")
        with self._db.cursor() as cur:
            try:
                yield cur
            except Exception:
                self._db.rollback()
                raise
            else:
                self._db.commit()

    def open(self) -> Self:
        self._db = psycopg.connect(
            host=self._settings.host,
            port=self._settings.port,
            user=self._settings.user,
            password=self._settings.password,
            dbname=self._settings.name,
            row_factory=dict_row,
        )
        return self

    def close(self) -> None:
        if self._db is None:
            return
        self._db.close()

    def get(self, id: UUID) -> Topic:
        with self._get_cursor() as cur:
            record = cur.execute(
                "SELECT * FROM topic WHERE id = %s LIMIT 1",
                (id,),
            ).fetchone()
        if record is None:
            raise TopicNotFoundError
        return Topic(**record)

    def create(self, topic: Topic) -> None:
        with self._get_cursor() as cur:
            try:
                cur.execute(
                    "INSERT INTO topic (id, content, priority, discussed) VALUES (%s, %s, %s, %s)",
                    (topic.id, topic.content, topic.priority, topic.discussed),
                )
            except psycopg.errors.UniqueViolation:
                raise TopicAlreadyExistsError

    def update(self, topic: Topic) -> None:
        raise NotImplementedError

    def list(self) -> list[Topic]:
        with self._get_cursor() as cur:
            return [Topic(**record) for record in cur.execute("SELECT * FROM topic")]
