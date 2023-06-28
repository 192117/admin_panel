from psycopg2.extensions import connection as _connection
from state_etl import JsonFileStorage


class PostgresExtract:
    """Class for extracting data from PostgreSQL database. """

    def __init__(self, connection: _connection, time: str, size: int, state: JsonFileStorage):
        """Initializes a PostgresExtract instance.

        :param connection: The PostgreSQL connection object.
        :param time: The timestamp used for data extraction.
        :param size: The size of data to extract in each iteration.
        :param state: The state storage object.
        """
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.time = time
        self.size = size
        self.state = state

    def producer(self):
        """Extracts persons data from PostgreSQL and saves it to the state storage."""
        offset = 0
        persons = []
        state_values = self.state.retrieve_state()
        if state_values['stage'] == '':
            while True:
                self.cursor.execute(f'SELECT id, modified FROM content.person '
                                    f'WHERE modified <= to_timestamp(\'{self.time}\', \'YYYY-MM-DD HH24:MI:SS\') '
                                    f'ORDER BY modified LIMIT {self.size} OFFSET {offset};')
                values = self.cursor.fetchall()
                if len(values) != 0:
                    persons.extend([values[0] for values in values])
                    offset += self.size
                else:
                    break
            self.state.save_state({'stage': 'producer', 'values': persons})

    def enricher(self):
        """Enriches the data with film_works and saves it to the state storage."""
        offset = 0
        film_works = []
        state_values = self.state.retrieve_state()
        if state_values['stage'] == 'producer':
            persons = ', '.join(f'\'{str(person)}\'' for person in state_values['values'])
            while True:
                self.cursor.execute(f'SELECT fw.id, fw.modified FROM content.film_work fw '
                                    f'LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id '
                                    f'WHERE pfw.person_id IN ({persons}) OR pfw.person_id ISNULL '
                                    f'ORDER BY fw.modified LIMIT {self.size} OFFSET {offset};')
                values = self.cursor.fetchall()
                if len(values) != 0:
                    film_works.extend([values[0] for values in values])
                    offset += self.size
                else:
                    break
            self.state.save_state({'stage': 'enricher', 'values': film_works})

    def merger(self, offset: int = 0):
        """Merges the data and saves it to the state storage.

        :param offset: The offset value for data extraction.
        """
        state_values = self.state.retrieve_state()
        if state_values['stage'] == 'enricher':
            film_works = ', '.join(f'\'{str(film_work)}\'' for film_work in state_values['values'])
        elif state_values['stage'] == 'elastic':
            film_works = state_values['other_values']
        self.cursor.execute(f'SELECT fw.id as id, fw.rating as imdb_rating, '
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
                            f'filter ( where pfw.role = \'writer\' ) as writers, '
                            f'json_agg(distinct jsonb_build_object(\'id\', g.id, \'name\', g.name)) as genres_list '
                            f'FROM content.film_work fw '
                            f'LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id '
                            f'LEFT JOIN content.person p ON p.id = pfw.person_id '
                            f'LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id '
                            f'LEFT JOIN content.genre g ON g.id = gfw.genre_id '
                            f'WHERE fw.id IN ({film_works}) '
                            f'GROUP BY fw.id LIMIT {self.size} OFFSET {offset};')
        values = self.cursor.fetchall()
        if values:
            self.state.save_state({'stage': 'merger', 'values': values, 'other_values': film_works})
        else:
            self.state.save_state({'stage': 'merger', 'values': values})

    def merger_genres(self, offset: int = 0):
        """Merges the data and saves it to the state storage.

        :param offset: The offset value for data extraction.
        """
        state_values = self.state.retrieve_state()
        if state_values['stage'] == '' or state_values['stage'] == 'elastic':
            self.cursor.execute(f'SELECT id, name, description FROM content.genre '
                                f'WHERE modified <= to_timestamp(\'{self.time}\', \'YYYY-MM-DD HH24:MI:SS\') '
                                f'ORDER BY modified LIMIT {self.size} OFFSET {offset};')
            values = self.cursor.fetchall()
            self.state.save_state({'stage': 'merger', 'values': values})

    def merger_persons(self, offset: int = 0):
        """Merges the data and saves it to the state storage.

        :param offset: The offset value for data extraction.
        """
        state_values = self.state.retrieve_state()
        if state_values['stage'] == '' or state_values['stage'] == 'elastic':
            self.cursor.execute(f'SELECT p.id AS id, p.full_name AS full_name, '
                                f'json_agg(json_build_object(\'id\', pfw.film_work_id, \'roles\', pfw.roles)) AS films '
                                f'FROM content.person p '
                                f' LEFT JOIN (SELECT pfw.person_id, pfw.film_work_id, '
                                f'array_agg(DISTINCT pfw.role) AS roles FROM content.person_film_work pfw '
                                f'GROUP BY pfw.person_id, pfw.film_work_id) pfw ON pfw.person_id = p.id '
                                f'WHERE p.modified <= to_timestamp(\'{self.time}\', \'YYYY-MM-DD HH24:MI:SS\') '
                                f'GROUP BY p.id LIMIT {self.size} OFFSET {offset};')
            values = self.cursor.fetchall()
            self.state.save_state({'stage': 'merger', 'values': values})
