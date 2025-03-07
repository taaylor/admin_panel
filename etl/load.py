import logging

import config
from backoff import backoff
from elasticsearch import Elasticsearch, exceptions, helpers
from transform import Movie


@backoff(exception=(exceptions.ConnectionError))
def loader_elasticsearch(data: list[Movie]) -> None:
    els = Elasticsearch(config.ELASTICSEARCH)

    values = [
        {"_index": "movies", "_id": movie.id, "_source": movie.model_dump()}
        for movie in data
    ]

    for success, info in helpers.streaming_bulk(els, values):
        if not success:
            logging.warning(f"Ошибка при загрузке данных в Elasticsearch: {info}")
    logging.info("Данные успешно загружены в Elasticsearch")
