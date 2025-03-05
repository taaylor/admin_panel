from pydantic import BaseModel, BeforeValidator
from typing import List, Dict, Any
from typing_extensions import Annotated

def _convert_str(value: set) -> str:
    return ', '.join(value)

def _convert_list(value: set) -> list:
    return list(value)

class Movie(BaseModel):
    id: str
    imdb_rating: float
    genres: Annotated[List[str], BeforeValidator(_convert_list)]
    title: str
    description: str
    directors_names: Annotated[str, BeforeValidator(_convert_str)]
    actors_names: Annotated[str, BeforeValidator(_convert_str)]
    writers_names: Annotated[str, BeforeValidator(_convert_str)]
    directors: Annotated[List[Dict[str, str]], BeforeValidator(_convert_list)]
    actors: Annotated[List[Dict[str, str]], BeforeValidator(_convert_list)]
    writers: Annotated[List[Dict[str, str]], BeforeValidator(_convert_list)]

    def transform_data(data: List[dict[str, Any]]) -> List['Movie']:
        """ Преобразует сырые данные из Postgres в список объектов Movie """

        movies = dict()

        for item in data:
            movies_id = str(item.get('fw_id'))
            
            if movies_id not in movies:
                movies[movies_id] = {
                    'id': movies_id,
                    'imdb_rating': item.get('rating'),
                    'genres': set(),
                    'title': item.get('title'),
                    'description': item.get('description'),
                    'directors_names': set(),
                    'actors_names': set(),
                    'writers_names': set(),
                    'directors': list(),
                    'actors': list(),
                    'writers': list()
                }

            movie = movies.get(movies_id)

            if gen := item.get('name'):
                movie['genres'].add(gen)

            person = {'id': str(item.get('id')), 'name': item.get('full_name')}
            if item.get('role') == 'actor':
                movie['actors_names'].add(person['name'])
                if person not in movie['actors']:
                    movie['actors'].append(person) 
            elif item.get('role') == 'writer':
                movie['writers_names'].add(person['name'])
                if person not in movie['writers']:
                    movie['writers'].append(person)
            elif item.get('role') == 'director':
                movie['directors_names'].add(person['name'])
                if person not in movie['directors']:
                    movie['directors'].append(person)

        movies_data = [Movie(**value) for value in movies.values()]
        return movies_data


        







        