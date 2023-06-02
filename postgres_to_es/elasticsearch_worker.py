import json

from configuration import logger


class ElasticWorker:

    def __init__(self, es, state, index_name, path_schema, path_data_to_es):
        self.es = es
        self.state = state
        self.index_name = index_name
        self.path_schema = path_schema
        self.path_data = path_data_to_es

    def make_schema(self):
        if not self.es.indices.exists(index=self.index_name):
            with open(self.path_schema, 'r') as file:
                schema = json.load(file)
                self.es.indices.create(index=self.index_name, body=schema)
                logger.info('Created index in ES!')

    def load_data(self):
        state_values = self.state.retrieve_state()
        if state_values['stage'] == 'transform':
            with open(self.path_data, 'r') as file:
                data = json.load(file)
                self.es.bulk(index=self.index_name, body=data)
                logger.info('Data successfully uploaded to ES!')
            self.state.save_state(
                {'stage': 'elastic', 'values': state_values['values'], 'film_works': state_values['film_works']},
            )
