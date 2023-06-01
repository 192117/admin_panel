import datetime
import os
import time

import backoff
import elasticsearch
import psycopg2
from configuration import dsl, es_dsl, es_size, logger
from data_from_postgres.extract import extract_merger
from elasticsearch.exceptions import ConnectionError, ConnectionTimeout
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from save_to_es import save_data_es
from schema_es.create_schema import make_or_check_schema
from state import get_state, save_state
from transform.transform_data import make_json_to_es, make_list_dataclass


@backoff.on_exception(backoff.expo, (ConnectionError, ConnectionTimeout, psycopg2.Error), max_tries=10)
def psql_to_es(pg_conn: _connection, es: elasticsearch.Elasticsearch, size):
    try:
        make_or_check_schema(es)
        if get_state() is None:
            save_state()
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        state = get_state()
        if now > state['last_date']:
            offset = 0
            while True:
                values = extract_merger(pg_conn, now, size, offset)
                if len(values) != 0:
                    make_json_to_es(make_list_dataclass(values), os.environ.get('ELASTIC_SCHEME'))
                    save_data_es(es, os.environ.get('ELASTIC_SCHEME'))
                else:
                    break
                offset += size
    except FileNotFoundError as exception:
        logger.error(exception)
    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as exception:
        logger.error(exception)


if __name__ == '__main__':
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn, \
            elasticsearch.Elasticsearch(es_dsl) as es:
        while True:
            logger.info('Data loading process started in ES!')
            psql_to_es(pg_conn, es, es_size)
            time.sleep(10)
