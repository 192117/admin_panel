import abc
import json
from typing import Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Save the state to persistent storage."""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Load the state locally from persistent storage."""
        pass


class JsonFileStorage(BaseStorage):
    """Storage implementation using a JSON file."""
    def __init__(self, file_path: Optional[str] = 'state.json'):
        """Initialize a JsonFileStorage instance.

        :param file_path: The path to the JSON file. Defaults to 'state.json'.
        """
        self.file_path = file_path

    def retrieve_state(self):
        """Save the state to persistent storage."""
        try:
            with open(self.file_path, 'r') as readfile:
                state = json.load(readfile)
        except FileNotFoundError:
            state = {}
        return state

    def save_state(self, state: dict):
        """Load the state locally from persistent storage.

        :param state: The state dictionary to save.
        :return: The loaded state dictionary.
        """
        with open(self.file_path, 'w') as writefile:
            json.dump(state, writefile)
