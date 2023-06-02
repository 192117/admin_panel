import logging
import os

from dotenv import load_dotenv

env_path = './movies_admin/config/.env'
load_dotenv(os.path.abspath(env_path))


dsl = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'options': '-c search_path=public,content',
}
es_dsl = [{
    'host': os.getenv('ELASTIC_HOST'),
    'port': int(os.getenv('ELASTIC_PORT')),
    'scheme': os.getenv('ELASTIC_SCHEME'),
}]
es_size = int(os.getenv('ES_SIZE'))

logging.basicConfig(
    filename='ETL.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
)

logger = logging.getLogger()
