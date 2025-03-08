import logging
import time
from contextlib import closing

import config
import psycopg
from backoff import backoff
from extract import PostgresExtract
from load import loader_elasticsearch
from redis import Redis, exceptions
from state import RedisStorage, State
from transform import Movie

settings = config.ConfigApp()
settings.start_log()


@backoff(exception=(psycopg.Connection, exceptions.ConnectionError))
def main():
    with closing(
        psycopg.connect(**settings.postgres.model_dump())
    ) as psql_conn, closing(Redis(**settings.redis.model_dump())) as redis_conn:

        while True:
            state = State(RedisStorage(redis_adapter=redis_conn))
            data_extract = PostgresExtract(psql_conn, state)
            data, states = data_extract.get_updated_films()

            if not data:
                logging.info("Нет новых данных для обновления в Elasticsearch")
            else:
                transform_data: list[Movie] = Movie.transform_data(data)

                loader_elasticsearch(transform_data)
                state.update_states(states)
                logging.info("Данные успешно обработаны ;)")

            time.sleep(15)


if __name__ == "__main__":
    main()
