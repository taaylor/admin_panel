import logging
import os

import dotenv
from pydantic import ConfigDict, model_validator
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    user: str
    password: str
    host: str
    port: int
    dbname: str

    model_config = ConfigDict(
        env_prefix="POSTGRES_", env_file=dotenv.find_dotenv(), extra="ignore"
    )


class RedisSettings(BaseSettings):
    host: str
    port: int
    decode_responses: bool = True

    model_config = ConfigDict(
        env_prefix="REDIS_", env_file=dotenv.find_dotenv(), extra="ignore"
    )


class ElasticsearchSettings(BaseSettings):
    host: str
    port: int
    url_elastic: str = ""

    model_config = ConfigDict(
        env_prefix="ELASTIC_", env_file=dotenv.find_dotenv(), extra="ignore"
    )

    @model_validator(mode="after")
    def set_url_elastic(self) -> "ElasticsearchSettings":
        self.url_elastic = f"http://{self.host}:{self.port}/"
        return self


class ConfigApp(BaseSettings):
    debug: bool
    log_dir: str = "logs"
    null_uuid: list[str] = ["00000000-0000-0000-0000-000000000000"]

    redis_key_storage: str = "storage"
    redis_person_state: str = "person_state"
    redis_genre_state: str = "genre_state"
    redis_fw_state: str = "film_work_state"

    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()
    elasticsearch: ElasticsearchSettings = ElasticsearchSettings()

    class Config:
        env_file = dotenv.find_dotenv()
        extra = "ignore"

    def start_log(self) -> None:
        os.makedirs(self.log_dir, exist_ok=True)
        log_file = os.path.join(self.log_dir, "app.log")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
