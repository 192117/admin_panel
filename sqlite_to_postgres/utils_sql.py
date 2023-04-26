from sqlite_to_postgres.dataclasses_for_db import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork

FROM_TABLES = {
    'film_work': 'SELECT id, title, description, creation_date, rating, "type", created_at, updated_at FROM film_work;',
    'genre': 'SELECT id, "name", description, created_at, updated_at FROM genre;',
    'person': 'SELECT id, full_name, created_at, updated_at FROM person;',
    'genre_film_work': 'SELECT id, film_work_id, genre_id, created_at FROM genre_film_work;',
    'person_film_work': 'SELECT id, film_work_id, person_id, "role", created_at FROM person_film_work;',
}

TABLES = ['film_work', 'genre', 'person', 'genre_film_work', 'person_film_work']

TO_TABLES = {
    'film_work': (
        'id', 'title', 'description', 'creation_date', 'rating', 'type', 'created', 'modified',
    ),
    'genre': (
        'id', 'name', 'description', 'created', 'modified',
    ),
    'person': (
        'id', 'full_name', 'created', 'modified',
    ),
    'genre_film_work': (
        'id', 'film_work_id', 'genre_id', 'created',
    ),
    'person_film_work': (
        'id', 'film_work_id', 'person_id', 'role', 'created',
    ),
}

DATACLASSES_DB = {
    'film_work': Filmwork,
    'genre': Genre,
    'person': Person,
    'genre_film_work': GenreFilmwork,
    'person_film_work': PersonFilmwork,
}

TEST_SQLite = {
    'film_work': 'SELECT id, title, description, rating, "type", created_at, updated_at FROM film_work ORDER BY id;',
    'genre': 'SELECT id, "name", description, created_at, updated_at FROM genre ORDER BY id;',
    'person': 'SELECT id, full_name, created_at, updated_at FROM person ORDER BY id;',
    'genre_film_work': 'SELECT id, film_work_id, genre_id, created_at FROM genre_film_work ORDER BY id;',
    'person_film_work': 'SELECT id, film_work_id, person_id, "role", created_at FROM person_film_work ORDER BY id;',
}
TEST_PostgreSQL = {
    'film_work': 'SELECT id, title, description, rating, "type", created, modified FROM film_work ORDER BY id;',
    'genre': 'SELECT id, "name", description, created, modified FROM genre ORDER BY id;',
    'person': 'SELECT id, full_name, created, modified FROM person ORDER BY id;',
    'genre_film_work': 'SELECT id, film_work_id, genre_id, created FROM genre_film_work ORDER BY id;',
    'person_film_work': 'SELECT id, film_work_id, person_id, "role", created FROM person_film_work ORDER BY id;',
}

SIZE = 100
