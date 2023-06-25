import uuid
from dataclasses import dataclass
from typing import Optional


@dataclass
class Genres:

    id: uuid.UUID
    name: str = ''
    description: Optional[str] = None

    def __post_init__(self):
        if self.description is None:
            self.description = ''


genre_atributes = [
    'id', 'name', 'description',
]
