import datetime
import json
import os


def get_state():
    try:
        with open(os.path.abspath('state.json'), 'r') as state_file:
            return json.load(state_file)
    except FileNotFoundError:
        return None


def save_state(stage=0):
    with open(os.path.abspath('state.json'), 'w') as state_file:
        date = {
            'last_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'stage': stage,
        }
        json.dump(date, state_file, ensure_ascii=False, indent=4)
