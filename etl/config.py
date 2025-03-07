import logging
import os

import redis
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler()],
)

REDIS = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    decode_responses=True,
)

DATABASE = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("SQL_HOST"),
    "port": os.getenv("SQL_PORT"),
}

ELASTICSEARCH = f"http://{os.getenv('ELASTIC_HOST')}:{os.getenv('ELASTIC_PORT')}"

# key state
PERSON_STATE = "person_state"
GENRE_STATE = "genre_state"
FW_STATE = "film_work_state"

NULL_ID = ["00000000-0000-0000-0000-000000000000"]
