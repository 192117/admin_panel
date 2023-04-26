import uuid
from dataclasses import dataclass, field


@dataclass
class Genre:

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    name: str = ''
    description: str = ''
    created: str = 'NOW()'
    modified: str = 'NOW()'

    def __post_init__(self):
        if self.created is None:
            self.created = 'NOW()'
        if self.modified is None:
            self.modified = 'NOW()'


@dataclass
class Filmwork:

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    title: str = ''
    description: str = ''
    creation_date: str = 'NOW()'
    rating: float = field(default=0.0)
    type: str = field(default='movie')
    created: str = 'NOW()'
    modified: str = 'NOW()'

    def __post_init__(self):
        if self.creation_date is None:
            self.creation_date = 'NOW()'
        if self.created is None:
            self.created = 'NOW()'
        if self.modified is None:
            self.modified = 'NOW()'


@dataclass
class Person:

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    full_name: str = ''
    created: str = 'NOW()'
    modified: str = 'NOW()'

    def __post_init__(self):
        if self.created is None:
            self.created = 'NOW()'
        if self.modified is None:
            self.modified = 'NOW()'


@dataclass
class GenreFilmwork:

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: Filmwork = ''
    genre_id: Genre = ''
    created: str = 'NOW()'

    def __post_init__(self):
        if self.created is None:
            self.created = 'NOW()'


@dataclass
class PersonFilmwork:

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    film_work_id: Filmwork = ''
    person_id: Person = ''
    role: str = ''
    created: str = 'NOW()'

    def __post_init__(self):
        if self.created is None:
            self.created = 'NOW()'
