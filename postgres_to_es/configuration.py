import logging
import os

from dotenv import load_dotenv
from postgres_to_es.genres.dataclass_for_trans import Genres, genre_atributes
from postgres_to_es.movies.dataclass_for_trans import Movies, movie_atributes
from postgres_to_es.persons.dataclass_for_trans import Persons, person_atributes

# env_path = '../../movies_admin/config/.env'  # for local run
env_path = '././movies_admin/config/.env'  # for docker run
load_dotenv(os.path.abspath(env_path))


dsl = {
    'dbname': os.getenv('POSTGRES_DB'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'options': '-c search_path=public,content',
}
es_dsl_movies = [{
    'host': os.getenv('ELASTIC_HOST'),
    'port': int(os.getenv('ELASTIC_PORT')),
    'scheme': os.getenv('ELASTIC_SCHEME_MOVIES'),
}]
es_dsl_genres = [{
    'host': os.getenv('ELASTIC_HOST'),
    'port': int(os.getenv('ELASTIC_PORT')),
    'scheme': os.getenv('ELASTIC_SCHEME_GENRES'),
}]
es_dsl_persons = [{
    'host': os.getenv('ELASTIC_HOST'),
    'port': int(os.getenv('ELASTIC_PORT')),
    'scheme': os.getenv('ELASTIC_SCHEME_PERSONS'),
}]
dataclasses_dict = {
    'movies': Movies,
    'genres': Genres,
    'persons': Persons,
}
dataclasses_atribute = {
    'movies': movie_atributes,
    'genres': genre_atributes,
    'persons': person_atributes,
}
es_size = int(os.getenv('ES_SIZE'))

logging.basicConfig(
    filename='ETL.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
)

logger = logging.getLogger()
