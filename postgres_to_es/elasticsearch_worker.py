import json

from postgres_to_es.configuration import logger


class ElasticWorker:
    """Class for working with Elasticsearch."""

    def __init__(self, es, state, index_name, path_schema, path_data_to_es):
        """Initializes an ElasticWorker instance.

        :param es: The Elasticsearch client.
        :param state: The state storage object.
        :param index_name: The name of the Elasticsearch index.
        :param path_schema: The path to the schema file.
        :param path_data_to_es: The path to the data file.
        """
        self.es = es
        self.state = state
        self.index_name = index_name
        self.path_schema = path_schema
        self.path_data = path_data_to_es

    def make_schema(self):
        """Creates the Elasticsearch index using the schema file."""
        if not self.es.indices.exists(index=self.index_name):
            with open(self.path_schema, 'r') as file:
                schema = json.load(file)
                self.es.indices.create(index=self.index_name, body=schema)
                logger.info(f'Created {self.index_name} index in ES!')

    def load_data(self):
        """Loads the transformed data to Elasticsearch."""
        state_values = self.state.retrieve_state()
        if state_values['stage'] == 'transform':
            with open(self.path_data, 'r') as file:
                data = json.load(file)
                self.es.bulk(index=self.index_name, body=data)
                logger.info('Data successfully uploaded to ES!')
            try:
                self.state.save_state({'stage': 'elastic', 'other_values': state_values['other_values']})
            except KeyError:
                self.state.save_state({'stage': 'elastic', 'values': []})
