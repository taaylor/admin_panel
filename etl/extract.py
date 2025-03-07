import datetime
import logging
from contextlib import closing
from typing import Any, Literal
from uuid import UUID

import config
import psycopg
import psycopg.rows
import redis
import redis.exceptions
from backoff import backoff
from state import State


def _get_ids_and_state_table(
    cursor: psycopg.Cursor, table: Literal["person", "genre"], state: State
) -> tuple[list[UUID], datetime.datetime]:
    query = f""" 
        SELECT id, modified 
        FROM content.{table}
        WHERE modified > %s
        ORDER BY modified ASC
        LIMIT 100;
    """
    last_state = (
        state.get_state(config.PERSON_STATE)
        if table == "person"
        else state.get_state(config.GENRE_STATE)
    )
    request = cursor.execute(query, (last_state,))
    result = request.fetchall()

    if not result:
        return [], last_state

    ids = list(i[0] for i in result)
    stat = result[-1][1]
    return ids, stat


def _get_updated_person_and_genre(
    connect: psycopg.Connection, state: State
) -> tuple[tuple, tuple]:
    with closing(connect.cursor()) as psql_cursor:
        person: tuple[list[UUID], datetime.datetime] = _get_ids_and_state_table(
            cursor=psql_cursor, table="person", state=state
        )
        genre: tuple[list[UUID], datetime.datetime] = _get_ids_and_state_table(
            cursor=psql_cursor, table="genre", state=state
        )
        return person, genre


def _get_updated_film_work(
    connect: psycopg.Connection, state: State
) -> tuple[list[UUID], dict[str, str]]:
    query = """
        select fw.id, fw.modified
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        WHERE pfw.person_id = ANY(
            %s
        ) 
        OR gfw.genre_id = ANY(
            %s   
        ) 
        OR fw.modified > %s
        group by fw.id
        ORDER BY fw.modified asc
        LIMIT 100 
    """
    person, genre = _get_updated_person_and_genre(connect, state)
    last_state_fw = state.get_state(config.FW_STATE)
    with closing(connect.cursor()) as psql_cursor:
        request = psql_cursor.execute(query, (person[0], genre[0], last_state_fw))
        result = request.fetchall()

        states = {
            config.FW_STATE: last_state_fw,
            config.GENRE_STATE: genre[1],
            config.PERSON_STATE: person[1],
        }
        if not result:
            return [], states

        ids_fw = list(i[0] for i in result)
        states[config.FW_STATE] = result[-1][1]

        return ids_fw, states


class PostgresExtract:
    QUERY = """
        SELECT 
            fw.id as fw_id, 
            fw.title, 
            fw.description, 
            fw.rating, 
            fw.type, 
            COALESCE(
                json_agg(
                    DISTINCT jsonb_build_object(
                        'role', pfw.role,
                        'id', p.id,
                        'name', p.full_name
                    )
                ) FILTER (WHERE p.id is not null),
                '[]'
            ) AS persons,
            array_agg(DISTINCT g.name) AS genres
        FROM content.film_work fw
        LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
        LEFT JOIN content.person p ON p.id = pfw.person_id
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id
        WHERE fw.id = ANY(%s)
        GROUP BY fw.id
        ORDER BY fw.modified
        LIMIT 100;
    """

    def __init__(self, connection: psycopg.Connection, state: State) -> None:
        self.connection = connection
        self.state = state

    @backoff(exception=(psycopg.errors.DatabaseError, redis.exceptions.RedisError))
    def get_updated_films(self) -> tuple[list[dict[str, Any]], dict[str, str]]:

        ids_fw, states = _get_updated_film_work(self.connection, self.state)

        with closing(
            self.connection.cursor(row_factory=psycopg.rows.dict_row)
        ) as psql_cursor:
            request = psql_cursor.execute(self.QUERY, (ids_fw,))

            result = request.fetchall()
            logging.info("Получены фильмы из Postgres: %s шт.", len(result))
            return result, states
