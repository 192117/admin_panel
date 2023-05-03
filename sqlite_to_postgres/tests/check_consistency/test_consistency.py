import datetime
import os
import sqlite3

import psycopg2
from dotenv import load_dotenv

from sqlite_to_postgres.utils_sql import TABLES, TEST_PostgreSQL, TEST_SQLite


def test_check_lenght_tables():
    with psycopg2.connect(**dsl) as pg_conn:
        with sqlite3.connect(os.getenv('ABS_PATH_SQLITE')) as sqlite_conn:
            sqlite_cursor = sqlite_conn.cursor()
            pg_cursor = pg_conn.cursor()
            for table_name in TABLES:
                pg_cursor.execute(TEST_PostgreSQL[table_name])
                pg_result = pg_cursor.fetchall()

                sqlite_cursor.execute(TEST_SQLite[table_name])
                sqlite_result = sqlite_cursor.fetchall()

                assert len(pg_result) == len(sqlite_result)


def check_equal(row1, row2):
    for i in range(len(row1)):
        if isinstance(row2[i], datetime.datetime):
            assert datetime.datetime.fromisoformat(row1[i]) == row2[i]
        else:
            assert row1[i] == row2[i]


def test_check_consistency():
    with psycopg2.connect(**dsl) as pg_conn:
        with sqlite3.connect(os.getenv('ABS_PATH_SQLITE')) as sqlite_conn:
            sqlite_cursor = sqlite_conn.cursor()
            pg_cursor = pg_conn.cursor()
            for table_name in TABLES:
                pg_cursor.execute(TEST_PostgreSQL[table_name])
                sqlite_cursor.execute(TEST_SQLite[table_name])
                for sqlite_row, pg_row in zip(sqlite_cursor.fetchall(), pg_cursor.fetchall()):
                    check_equal(sqlite_row, pg_row)


if __name__ == '__main__':
    env_path = '../../../movies_admin/config/.env'
    load_dotenv(env_path)
    dsl = {
        'dbname': os.getenv('POSTGRES_DB'),
        'user': os.getenv('POSTGRES_USER'),
        'password': os.getenv('POSTGRES_PASSWORD'),
        'host': os.getenv('POSTGRES_HOST'),
        'port': os.getenv('POSTGRES_PORT'),
        'options': '-c search_path=content',
    }
    test_check_lenght_tables()
    test_check_consistency()
