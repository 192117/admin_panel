import sqlite3
from dataclasses import dataclass
from typing import List


class PostgresSaver:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def save_all_data(self, data: List[dataclass], table_name: str) -> None:
        from sqlite_to_postgres.utils_sql import SIZE, TO_TABLES
        for i in range(0, len(data), SIZE):
            rows = data[i:i + SIZE]
            values = [tuple(row.__dict__.values()) for row in rows]
            sql_row = f"INSERT INTO {table_name} ({', '.join(TO_TABLES[table_name])}) VALUES " \
                      f"({','.join(['%s'] * len(TO_TABLES[table_name]))}) ON CONFLICT (id) DO NOTHING;"
            self.cursor.executemany(sql_row, values)


class SQLiteLoader:

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def load_movies(self, table_name: str) -> List[dataclass]:
        from sqlite_to_postgres.utils_sql import DATACLASSES_DB, FROM_TABLES, TO_TABLES
        self.cursor.execute(FROM_TABLES[table_name])
        data = self.cursor.fetchall()
        answer = []
        for row in data:
            table_class = DATACLASSES_DB[table_name]
            dict_values = dict(zip(TO_TABLES[table_name], row))
            answer.append(table_class(**dict_values))
        return answer
