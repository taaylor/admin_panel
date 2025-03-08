import abc
import json
import logging
from datetime import datetime
from typing import Any, Dict

import config
import redis
import redis.exceptions

settings = config.ConfigApp()


class BaseStorage(abc.ABC):
    """Абстрактное хранилище состояния."""

    @abc.abstractmethod
    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""

    @abc.abstractmethod
    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""


class RedisStorage(BaseStorage):
    """Реализация хранилища, использующего redis"""

    def __init__(self, redis_adapter: redis.Redis) -> None:
        self.redis_adapter = redis_adapter

    def save_state(self, state: Dict[str, Any]) -> None:
        """Сохранить состояние в хранилище."""
        json_state = json.dumps(state)
        self.redis_adapter.set(settings.redis_key_storage, json_state)

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        try:
            data = self.redis_adapter.get(settings.redis_key_storage)
            if data is None:
                return {}
            convert_dict = json.loads(data)
            return convert_dict
        except json.JSONDecodeError:
            logging.error("Ошибка декодирования JSON в retrieve_state")
            return {}


class State:
    """Класс для работы с состояниями."""

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа."""
        state = self.storage.retrieve_state()
        state[key] = str(value)
        self.storage.save_state(state)

    def get_state(self, key: str) -> Any:
        state = self.storage.retrieve_state().get(key)
        if not state or state == "None":
            return datetime.min
        logging.info("Состояние успешно получено из хранилища.")
        return state

    def update_states(self, states: dict[str, str]) -> None:
        for key, value in states.items():
            self.set_state(key, value)
            logging.info(f"Состояние - '{key}' успешно сохранилось в хранилище.")
