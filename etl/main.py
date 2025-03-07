import psycopg
import config
from extract import PostgresExtract
from contextlib import closing
from state import State, RedisStorage
from transform import Movie
import logging
from backoff import backoff
import time
from load import loader_elasticsearch

@backoff(exception=(psycopg.Connection,))
def main():
    with closing(psycopg.connect(**config.DATABASE)) as psql_conn:
        while True:
            state = State(RedisStorage(redis_adapter=config.REDIS))
            data_extract = PostgresExtract(psql_conn, state) 
            data, states = data_extract.get_updated_films()

            if not data:
                logging.info('Нет новых данных для обновления в Elasticsearch')
            else:
                transform_data: list[Movie] = Movie.transform_data(data)

                loader_elasticsearch(transform_data)
                state.update_states(states)
                logging.info('Данные успешно обработаны ;)')
            
            time.sleep(15)

if __name__ == "__main__":
    main()
        
