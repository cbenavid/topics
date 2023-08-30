from dataclasses import dataclass, field
from uuid import UUID


def _check_priority(priority: int) -> None:
    if priority <= 0:
        raise ValueError("Priority must be greater than zero")


@dataclass(kw_only=True)
class Topic:
    id: UUID
    content: str
    priority: int = field(default=1)

    def __post_init__(self) -> None:
        _check_priority(self.priority)
