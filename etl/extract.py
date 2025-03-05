import abc
import datetime
import logging
from contextlib import closing
from typing import Generator, Literal

import psycopg
import psycopg.rows
import redis
import redis.exceptions

import config
from backoff import backoff
from state import State


class InitMixin(abc.ABC):
    def __init__(self, connection: psycopg.Connection, state: State):
        self.connection = connection
        self.state = state


class GetUpdateObjectMixin(InitMixin):

    def _get_ids_update_object(
        self, table: Literal["person", "genre"], key_state: str
    ) -> tuple[list, datetime.datetime]:
        """Получаем id всех измененных объектов"""

        with closing(self.connection.cursor()) as psql_cursor:
            # получаем последнее состояние
            time = self.state.get_state(key_state)
            query = f"""
                SELECT id, modified
                FROM content.{table}
                WHERE modified > '{time}'
                ORDER BY modified
                LIMIT 100;
            """
            psql_cursor.execute(query)
            result = psql_cursor.fetchall()
            # получаем состояние из БД
            state = None
            if result:
                state = result[-1][1]
                print(state)
            # формируем ids из полученного результата
            ids = list(i[0] for i in result)
            return ids, state


class PostgresProducer(GetUpdateObjectMixin):
    def get_person_update_ids(self) -> tuple[list, datetime.datetime]:
        """Получаем id измененных person, состояние"""
        person = self._get_ids_update_object(
            table="person", key_state=config.PERSON_STATE
        )
        return person

    def get_genre_update_ids(self) -> tuple[list, datetime.datetime]:
        """Получаем id измененных genre, состояние"""
        genre = self._get_ids_update_object(
            table="genre", key_state=config.GENRE_STATE
        )
        return genre


class PostgresEnricher(InitMixin):
    def get_film_work_based_on_related_table(
        self,
    ) -> tuple[list, dict[str, datetime.datetime]]:
        with closing(self.connection.cursor()) as psql_cursor:
            time = self.state.get_state(config.FW_STATE)

            query = """
                SELECT fw.id, fw.modified
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                WHERE pfw.person_id = ANY(%s) OR gfw.genre_id = ANY(%s) OR fw.modified > %s
                ORDER BY fw.modified
                LIMIT 100;
            """
            producer = PostgresProducer(self.connection, self.state)
            ids_person, person_state = producer.get_person_update_ids()
            ids_genre, genre_state = producer.get_genre_update_ids()
            values = (ids_person or config.NULL_ID, ids_genre or config.NULL_ID, time)
            psql_cursor.execute(query, values)
            result = psql_cursor.fetchall()

            fw_state = None
            if result:
                fw_state = result[-1][1]
                print(fw_state)

            film_work_ids = list(i[0] for i in result)

            states = {
                config.PERSON_STATE: person_state,
                config.GENRE_STATE: genre_state,
                config.FW_STATE: fw_state,
            }

            return film_work_ids, states


class PostgresMerge(InitMixin):
    @backoff(exception=(psycopg.errors.DatabaseError, redis.exceptions.RedisError))
    def get_update_film_work(self) -> tuple[list, dict]:
        ''' возвращает список измененных фильмов '''

        with closing(self.connection.cursor(row_factory=psycopg.rows.dict_row)) as psql_cursor:
            query = """
                SELECT fw.id as fw_id, fw.title, fw.description, fw.rating, 
                    fw.type, pfw.role, p.id, p.full_name, g.name
                FROM content.film_work fw
                LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                WHERE fw.id = ANY(%s);
            """
            enricher = PostgresEnricher(self.connection, self.state)
            ids_fw, states = enricher.get_film_work_based_on_related_table()

            value = (ids_fw or config.NULL_ID,)

            psql_cursor.execute(query, value)

            res = psql_cursor.fetchall()
            
            return res, states
        
