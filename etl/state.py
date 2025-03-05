import abc
import json
import logging
from typing import Any, Dict

import redis
import redis.exceptions

from backoff import backoff


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
        self.redis_adapter.set("storage", json_state)
        logging.info("Состояние успешно сохранилось в хранилище.")

    def retrieve_state(self) -> Dict[str, Any]:
        """Получить состояние из хранилища."""
        try:
            data = self.redis_adapter.get("storage")
            if data is None:
                return {} 
            convert_dict = json.loads(data)
            logging.info("Состояние успешно получено из хранилища.")
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
        if not state or state == 'None':
            return '1970-01-01 00:00:00'
        return state
