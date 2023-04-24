import sqlite3
import os
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

from sqlite_to_postgres.loader_and_saver import PostgresSaver, SQLiteLoader
from sqlite_to_postgres.utils_sql import TABLES


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection, tables_from_sqlite: list):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)
    for table in tables_from_sqlite:
        data = sqlite_loader.load_movies(table)
        postgres_saver.save_all_data(data, table)


if __name__ == '__main__':
    env_path = '../movies_admin/config/.env'
    load_dotenv(env_path)
    dsl = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
    }
    try:
        with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn, TABLES)
    except (sqlite3.OperationalError, sqlite3.ProgrammingError) as error:
        print('Ошибка при выполнении операции в SQLite: ', error)
    except sqlite3.Error as error:
        print('Ошибка при работе с SQLite: ', error)
    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as error:
        print('Ошибка при выполнении операции в PostgreSQL: ', error)
    except psycopg2.Error as error:
        print('Ошибка при работе с PostgreSQL: ', error)
