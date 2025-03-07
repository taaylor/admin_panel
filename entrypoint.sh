#!/bin/bash

# Запускаем Elasticsearch
/usr/local/bin/docker-entrypoint.sh elasticsearch &

# Ждем, пока Elasticsearch станет доступен
until curl --silent --fail http://localhost:9200/_cluster/health; do
    echo "Ждём запуска Elasticsearch..."
    sleep 5
done

# Проверяем существует ли индекс movies
if ! curl --silent --fail -XGET "http://localhost:9200/movies"; then
    echo "Индекс 'movies' не найден, создаем..."
    curl -XPUT "http://localhost:9200/movies" -H "Content-Type: application/json" -d @/es_schema.json
else
    echo "Индекс 'movies' уже существует"
fi

wait -n
