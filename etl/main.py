import psycopg
import config
from extract import PostgresMerge
from contextlib import closing
from state import State, RedisStorage
from transform import Movie
import logging
import datetime
from backoff import backoff
from redis import exceptions
import time
from load import loader_elasticsearch


@backoff(exception=(exceptions.RedisError))
def save_state(state: State, states: dict[str, datetime.datetime]):
    for key, value in states.items():
        state.set_state(key, value)

def main():
    with closing(psycopg.connect(**config.DATABASE)) as psql_conn:
        storage = RedisStorage(redis_adapter=config.REDIS)
        state = State(storage=storage)
        result = PostgresMerge(
            connection=psql_conn, state=state
        )
        data, states = result.get_update_film_work()
        transform_data = Movie.transform_data(data)
        
        loader_elasticsearch(transform_data)
        
        # сохраняем состояние после загрузки данных в Elastic
        save_state(state=state, states=states)

        logging.info('Успех!')
         
            

if __name__ == "__main__":
    while True:
        main()
        time.sleep(10)
