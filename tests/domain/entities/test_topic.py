from uuid import UUID

import pytest

from topics.domain.entities.topic import Topic


class TestTopicEntity:
    def test_topic_can_be_created(self) -> None:
        topic = Topic(
            id=UUID("8623788e-3c9c-421c-ab10-92dd10405ebe"),
            content="Some ref",
            priority=1,
        )
        assert topic.id == UUID("8623788e-3c9c-421c-ab10-92dd10405ebe")
        assert topic.content == "Some ref"
        assert topic.priority == 1

    @pytest.mark.parametrize("priority", [-1, 0])
    def test_topic_priority_must_be_greater_than_zero(self, priority: int) -> None:
        with pytest.raises(ValueError, match="Priority must be greater than zero"):
            build_topic(priority=priority)

    def test_topic_has_default_priority_of_one(self) -> None:
        topic = build_topic()
        assert topic.priority == 1


def build_topic(
    id: UUID | None = None, content: str = "Some ref", priority: int | None = None
) -> Topic:
    id_ = id or UUID("8623788e-3c9c-421c-ab10-92dd10405ebe")
    extra_values = {}
    if priority is not None:
        extra_values["priority"] = priority
    return Topic(id=id_, content=content, **extra_values)
