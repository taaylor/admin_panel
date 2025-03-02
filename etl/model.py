from pydantic import BaseModel
from typing import List, Dict

class Movie(BaseModel):
    id: str
    imdb_rating: float
    genres: list
    title: str
    description: str
    directors_names: str
    actors_names: str
    writers_names: str
    directors: List[Dict[str, str]]
    actors: List[Dict[str, str]]
    writers: List[Dict[str, str]]