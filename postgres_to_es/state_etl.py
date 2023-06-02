import abc
import json
from typing import Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = 'state.json'):
        self.file_path = file_path

    def retrieve_state(self):
        try:
            with open(self.file_path, 'r') as readfile:
                state = json.load(readfile)
        except FileNotFoundError:
            state = {}
        return state

    def save_state(self, state: dict):
        with open(self.file_path, 'w') as writefile:
            json.dump(state, writefile)
