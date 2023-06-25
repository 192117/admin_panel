import uuid
from dataclasses import dataclass


@dataclass
class Persons:

    id: uuid.UUID
    full_name: str = ''


person_atributes = [
    'id', 'full_name',
]
