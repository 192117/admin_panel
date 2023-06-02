import json

from dataclass_for_trans import Movies, dataclass_atributes


class Transform:

    def __init__(self, index_name, path_data_to_es, state):
        self.index_name = index_name
        self.path_data = path_data_to_es
        self.state = state

    def _make_dataclass_list(self, values):
        return [Movies(**dict(zip(dataclass_atributes, row))) for row in values]

    def make_json_to_es(self):
        state_values = self.state.retrieve_state()
        if state_values['stage'] == 'merger' and len(state_values['values']) != 0:
            data = []
            for row in self._make_dataclass_list(state_values['values']):
                data.append({'index': {'_index': self.index_name, '_id': row.id}})
                data.append(row.__dict__)
            with open(self.path_data, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            self.state.save_state(
                {'stage': 'transform', 'values': state_values['values'], 'film_works': state_values['film_works']},
            )
