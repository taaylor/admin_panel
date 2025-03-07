from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Annotated, Any, Self
import logging
import uuid


class Movie(BaseModel):
    id: Annotated[uuid.UUID, Field(alias='fw_id')]
    imdb_rating: Annotated[float, Field(alias='rating')]
    title: str
    genres: list[str]
    description: str | None = None
    persons: list[dict[str, str]] = Field(exclude=True)
    directors_names: list[str] = Field(default_factory=list)
    actors_names: list[str] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)
    directors: list[dict[str, str]] = Field(default_factory=list)
    actors: list[dict[str, str]] = Field(default_factory=list)
    writers: list[dict[str, str]] = Field(default_factory=list)

    @model_validator(mode='after')
    def parse_persons(self) -> Self:
       
        for item in self.persons:
            person = {'id': item['id'], 'name': item['name']}
            
            if item.get('role') == 'director':
                self.directors.append(person)
                self.directors_names.append(person['name'])
            elif item.get('role') == 'writer':
                self.writers.append(person)
                self.writers_names.append(person['name'])
            elif item.get('role') == 'actor':
                self.actors.append(person)
                self.actors_names.append(person['name'])
        return self

    @classmethod
    def transform_data(cls, data: list[dict[str, Any]]) -> list['Movie']:
        transform_data = []
        for obj in data:
            try:
                transform_data.append(cls(**obj))
            except ValidationError as error:
                logging.warning(f'Пропущена невалидная запись UUID({obj.get('fw_id')}): {error}')
        
        logging.info('Данные прошли трансформацию успешно, кол-во - %s', len(transform_data))
        return transform_data
