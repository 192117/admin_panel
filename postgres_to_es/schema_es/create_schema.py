import json
import os

import elasticsearch


def make_or_check_schema(es: elasticsearch.Elasticsearch):
    if not es.indices.exists(index=os.environ.get('ELASTIC_SCHEME')):
        with open(os.path.abspath('schema_es/schema.json'), 'r') as file:
            schema = json.load(file)
            es.indices.create(index=os.environ.get('ELASTIC_SCHEME'), body=schema)
