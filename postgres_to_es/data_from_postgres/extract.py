import os

import psycopg2
from psycopg2.extensions import connection as _connection

from postgres_to_es.state import get_state


def extract_producer(pg_conn: _connection, time, size):
    try:
        cursor = pg_conn.cursor()
        offset = 0
        persons = []
        while True:
            cursor.execute(f'SELECT id, modified FROM content.person '
                           f'WHERE modified < to_timestamp(\'{time}\', \'YYYY-MM-DD HH24:MI:SS\') '
                           f'ORDER BY modified LIMIT {size} OFFSET {offset};')
            values = cursor.fetchall()
            if len(values) != 0:
                persons.extend(values)
                offset += size
            else:
                break
        return persons
    except (psycopg2.OperationalError, psycopg2.ProgrammingError):
        raise


def extract_enricher(pg_conn: _connection, time, size: int):
    try:
        cursor = pg_conn.cursor()
        persons = ', '.join(f'\'{str(person[0])}\'' for person in extract_producer(pg_conn, time, size))
        offset = 0
        film_works = []
        while True:
            cursor.execute(f'SELECT fw.id, fw.modified FROM content.film_work fw '
                           f'LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id '
                           f'WHERE pfw.person_id IN ({persons}) '
                           f'ORDER BY fw.modified LIMIT {size} OFFSET {offset};')
            values = cursor.fetchall()
            if len(values) != 0:
                film_works.extend(values)
                offset += size
            else:
                break
        return film_works
    except (psycopg2.OperationalError, psycopg2.ProgrammingError):
        raise


def extract_merger(pg_conn: _connection, time, size, offset: int = 0):
    try:
        cursor = pg_conn.cursor()
        if os.path.exists('state.json'):
            state = get_state()
            if state is None or state['stage'] == 0:
                film_works = ','.join(f'\'{str(film_work[0])}\'' for film_work in extract_enricher(pg_conn, time, size))
                cursor.execute(f'SELECT fw.id as id, fw.rating as imdb_rating, '
                               f'array_agg(distinct g.name) as genre, fw.title as title, '
                               f'fw.description as description, '
                               f'array_agg(distinct p.full_name) filter '
                               f'( where pfw.role = \'director\' ) as director,'
                               f'array_agg(distinct p.full_name) filter '
                               f'( where pfw.role = \'actor\' ) as actors_names,'
                               f'array_agg(distinct p.full_name) filter '
                               f'( where pfw.role = \'writer\' ) as writers_names,'
                               f'json_agg(distinct jsonb_build_object(\'id\', p.id, \'name\', p.full_name)) '
                               f'filter ( where pfw.role = \'actor\' ) as actors,'
                               f'json_agg(distinct jsonb_build_object(\'id\', p.id, \'name\', p.full_name)) '
                               f'filter ( where pfw.role = \'writer\' ) as writers '
                               f'FROM content.film_work fw '
                               f'LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id '
                               f'LEFT JOIN content.person p ON p.id = pfw.person_id '
                               f'LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id '
                               f'LEFT JOIN content.genre g ON g.id = gfw.genre_id '
                               f'WHERE fw.id IN ({film_works}) '
                               f'GROUP BY fw.id LIMIT {size} OFFSET {offset};')
                values = cursor.fetchall()
                return values
    except (psycopg2.OperationalError, psycopg2.ProgrammingError):
        raise
