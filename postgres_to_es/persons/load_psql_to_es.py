import datetime
import os
import time

import backoff
import elasticsearch
import psycopg2
from elasticsearch.exceptions import ConnectionError, ConnectionTimeout
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from postgres_to_es.configuration import dsl, es_dsl_persons, es_size, logger
from postgres_to_es.elasticsearch_worker import ElasticWorker
from postgres_to_es.persons.postgres_extract import PostgresExtract
from postgres_to_es.state_etl import JsonFileStorage
from postgres_to_es.tranform_data import Transform


@backoff.on_exception(backoff.expo, (ConnectionError, ConnectionTimeout, psycopg2.Error), max_tries=10)
def psql_to_es(pg_conn: _connection, es: elasticsearch.Elasticsearch, size):
    """Transfer data from PostgreSQL to Elasticsearch.

    :param pg_conn: The PostgreSQL connection object.
    :param es: The Elasticsearch client.
    :param size: The size of data to transfer in each iteration.
    """
    if not os.path.exists('persons_for_es.json'):
        data_for_es = open('persons_for_es.json', 'w')
        data_for_es.close()
    state = JsonFileStorage(file_path='persons_state.json')
    postgres_extract = PostgresExtract(
        connection=pg_conn,
        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        size=size,
        state=state,
    )
    transform = Transform(
        index_name=os.environ.get('ELASTIC_SCHEME_PERSONS'),
        path_data_to_es=os.path.abspath('persons_for_es.json'),
        state=state,
        schema=os.environ.get('ELASTIC_SCHEME_PERSONS'),
    )
    elastic_worker = ElasticWorker(
        es=es,
        state=state,
        index_name=os.environ.get('ELASTIC_SCHEME_PERSONS'),
        path_schema=os.path.abspath('persons_schema.json'),
        path_data_to_es=os.path.abspath('persons_for_es.json'),
    )
    if len(state.retrieve_state()) == 0:
        state.save_state({'stage': ''})
        elastic_worker.make_schema()
    offset = 0
    while True:
        stage_values = state.retrieve_state()
        if stage_values['stage'] == 'merger':
            if len(stage_values['values']) == 0:
                logger.info('Data loading persons process finished in ES!')
                state.save_state({'stage': ''})
                break
        postgres_extract.merger(offset)
        transform.make_json_to_es()
        elastic_worker.load_data()
        offset += size


if __name__ == '__main__':
    try:
        with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn, \
                elasticsearch.Elasticsearch(es_dsl_persons) as es:
            logger.info('Data loading persons process started in ES!')
            while True:
                psql_to_es(pg_conn, es, es_size)
                time.sleep(10)
                print('Persons done!')
    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as exception:
        logger.error(exception)
    except (ConnectionError, ConnectionTimeout) as exception:
        logger.error(exception)
    except FileNotFoundError as exception:
        logger.error(exception)
