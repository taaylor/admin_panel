import psycopg
import config
from extract import PostgresMerge
from contextlib import closing
from state import State, RedisStorage
import redis


def main():
    # with closing(psycopg.connect(**config.DATABASE)) as psql_conn:
    #     storage = RedisStorage(redis_adapter=config.REDIS)
    #     result = PostgresMerge(
    #         connection=psql_conn, state=State(storage=storage)
    #     )
    #     for r in result.get_update_film_work():
    #         print()
    #         print(r, sep='\n')
    #         break
    ...

if __name__ == "__main__":
    main()
