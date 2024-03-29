import json
from dataclasses import dataclass
from typing import Dict, List

from configuration import dataclasses_atribute, dataclasses_dict
from state_etl import JsonFileStorage


class Transform:
    """Class for transforming data and preparing it for Elasticsearch indexing."""

    def __init__(self, index_name: str, path_data_to_es: str, state: JsonFileStorage, schema: str = 'movies'):
        """Initializes a Transform instance.

        :param index_name: The name of the Elasticsearch index.
        :param path_data_to_es: The path to the data file.
        :param state: The state storage object.
        :param schema: The schema for Elasticsearch.
        """
        self.index_name = index_name
        self.path_data = path_data_to_es
        self.state = state
        self.schema = schema

    def _make_dataclass_list(self, values: List[Dict[str, str]]) -> list[dataclass]:
        """ Converts a list of dictionaries to a list of Movies/Genres/Persons dataclass instances.
        :param values: List of dictionaries to convert with data from PostgreSQL.
        :return: The list of Movies dataclass instances.
        """
        return [dataclasses_dict[self.schema](**dict(zip(dataclasses_atribute[self.schema], row))) for row in values]

    def make_json_to_es(self):
        """Transforms data into JSON format and saves it to a file."""
        state_values = self.state.retrieve_state()
        if state_values['stage'] == 'merger' and len(state_values['values']) != 0:
            data = []
            for row in self._make_dataclass_list(state_values['values']):
                data.append({'index': {'_index': self.index_name, '_id': row.id}})
                data.append(row.__dict__)
            with open(self.path_data, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            try:
                self.state.save_state({'stage': 'transform', 'other_values': state_values['other_values']})
            except KeyError:
                self.state.save_state({'stage': 'transform', 'values': []})
