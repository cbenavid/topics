from uuid import UUID

from topics.domain.entities.topic import Topic


class TestTopicEntity:
    def test_can_create_topic(self) -> None:
        topic = Topic(
            id=UUID("8623788e-3c9c-421c-ab10-92dd10405ebe"), content="Some ref"
        )
        assert topic.id == UUID("8623788e-3c9c-421c-ab10-92dd10405ebe")
        assert topic.content == "Some ref"
