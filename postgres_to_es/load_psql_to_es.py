import datetime
import os
import time

import backoff
import elasticsearch
import psycopg2
from configuration import dsl, es_dsl, es_size, logger
from elasticsearch.exceptions import ConnectionError, ConnectionTimeout
from elasticsearch_worker import ElasticWorker
from postgres_extract import PostgresExtract
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from state_etl import JsonFileStorage
from tranform_data import Transform


@backoff.on_exception(backoff.expo, (ConnectionError, ConnectionTimeout, psycopg2.Error), max_tries=10)
def psql_to_es(pg_conn: _connection, es: elasticsearch.Elasticsearch, size):
    if not os.path.exists('data_for_es.json'):
        data_for_es = open('data_for_es.json', 'w')
        data_for_es.close()
    state = JsonFileStorage()
    postgres_extract = PostgresExtract(
        connection=pg_conn,
        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        size=size,
        state=state,
    )
    transform = Transform(
        index_name=os.environ.get('ELASTIC_SCHEME'),
        path_data_to_es=os.path.abspath('data_for_es.json'),
        state=state,
    )
    elastic_worker = ElasticWorker(
        es=es,
        state=state,
        index_name=os.environ.get('ELASTIC_SCHEME'),
        path_schema=os.path.abspath('schema.json'),
        path_data_to_es=os.path.abspath('data_for_es.json'),
    )
    if len(state.retrieve_state()) == 0:
        state.save_state({'stage': ''})
        elastic_worker.make_schema()
    offset = 0
    while True:
        stage_values = state.retrieve_state()
        if stage_values['stage'] == 'merger':
            if len(stage_values['values']) == 0:
                logger.info('Data loading process finished in ES!')
                break
        postgres_extract.producer()
        postgres_extract.enricher()
        postgres_extract.merger(offset)
        transform.make_json_to_es()
        elastic_worker.load_data()
        offset += size


if __name__ == '__main__':
    try:
        with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn, \
                elasticsearch.Elasticsearch(es_dsl) as es:
            logger.info('Data loading process started in ES!')
            while True:
                psql_to_es(pg_conn, es, es_size)
                time.sleep(10)
    except (psycopg2.OperationalError, psycopg2.ProgrammingError) as exception:
        logger.error(exception)
    except (ConnectionError, ConnectionTimeout) as exception:
        logger.error(exception)
    except FileNotFoundError as exception:
        logger.error(exception)
