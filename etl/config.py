import logging
import os

import redis
from dotenv import load_dotenv

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

BATCH_SIZE = 100

DATABASE = {
    'dbname': 'movies_db', 
    'user': 'admin',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

# key state
PERSON_STATE = 'person_state'
GENRE_STATE = 'genre_state'
FW_STATE = 'film_work_state'



NULL_ID = ['00000000-0000-0000-0000-000000000000']