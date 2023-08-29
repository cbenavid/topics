from dataclasses import dataclass
from uuid import UUID


@dataclass
class Topic:
    id: UUID
    content: str
