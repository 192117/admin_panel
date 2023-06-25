import uuid
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Movies:

    id: uuid.UUID
    imdb_rating: Optional[float] = None
    genre: Optional[List] = None
    title: str = ''
    description: Optional[str] = None
    director: Optional[List] = None
    actors_names: Optional[List] = None
    writers_names: Optional[List] = None
    actors: Optional[List] = None
    writers: Optional[List] = None

    def __post_init__(self):
        if self.imdb_rating is None:
            self.imdb_rating = 0
        if self.description is None:
            self.description = ''
        if self.director is None:
            self.director = []
        if self.actors_names is None:
            self.actors_names = []
        if self.writers_names is None:
            self.writers_names = []
        if self.actors is None:
            self.actors = []
        if self.writers is None:
            self.writers = []


movie_atributes = [
    'id', 'imdb_rating', 'genre', 'title', 'description', 'director', 'actors_names', 'writers_names', 'actors',
    'writers',
]
