import json
import os

from transform.dataclass_for_trans import Movies, dataclass_atributes

from postgres_to_es.state import save_state


def make_list_dataclass(values):
    return [Movies(**dict(zip(dataclass_atributes, row))) for row in values]


def make_json_to_es(values, index_name):
    if len(values) != 0:
        data = []
        for row in values:
            data.append({'index': {'_index': index_name, '_id': row.id}})
            data.append(row.__dict__)
        with open(os.path.abspath('transform/data_for_es.json'), 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        save_state(1)
