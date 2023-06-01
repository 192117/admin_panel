import json
import os

import elasticsearch
from configuration import logger
from state import get_state, save_state


def save_data_es(es: elasticsearch.Elasticsearch, index_name):
    if os.path.exists(os.path.abspath('state.json')):
        state = get_state()
        if state['stage'] == 1:
            with open(os.path.abspath('transform/data_for_es.json'), 'r') as file:
                data = json.load(file)
                es.bulk(index=index_name, body=data)
                save_state()
                logger.info('Data successfully uploaded to ES!')
