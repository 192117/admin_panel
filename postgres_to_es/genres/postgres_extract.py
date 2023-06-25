from psycopg2.extensions import connection as _connection

from postgres_to_es.state_etl import JsonFileStorage


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

    def merger(self, offset: int = 0):
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
