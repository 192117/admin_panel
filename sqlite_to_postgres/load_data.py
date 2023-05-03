import logging
import os
import sqlite3

import psycopg2
from dotenv import load_dotenv
from loader_and_saver import PostgresSaver, SQLiteLoader
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from utils_sql import TABLES


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection, tables_from_sqlite: list):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)
    for table in tables_from_sqlite:
        values_from_sqlite = sqlite_loader.load_movies(table)
        dataclasses_values = sqlite_loader.values_to_dataclass(values_from_sqlite, table)
        postgres_saver.save_all_data(dataclasses_values, table)


if __name__ == '__main__':
    env_path = './movies_admin/config/.env'
    load_dotenv(env_path)
    dsl = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
        'options': '-c search_path=public,content',
    }
    try:
        with sqlite3.connect(os.getenv('ABS_PATH_SQLITE')) as sqlite_conn, \
                psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn, TABLES)
    except (sqlite3.OperationalError, sqlite3.ProgrammingError) as error:
        logging.error(f'Ошибка при выполнении операции в SQLite: {error}')
    except sqlite3.Error as error:
        logging.error(f'Ошибка при работе с SQLite: {error}')
    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as error:
        logging.error(f'Ошибка при выполнении операции в PostgreSQL: {error}')
    except psycopg2.Error as error:
        logging.error(f'Ошибка при работе с PostgreSQL: {error}')
