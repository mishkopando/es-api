from typing import Optional
from enum import Enum

from pydantic import BaseModel


class Writer(BaseModel):
    id: str
    name: str


class Actor(BaseModel):
    id: int
    name: str


class ShortMovie(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class Movie(ShortMovie):
    description: Optional[str]
    writers: Optional[list[Writer]]
    actors: Optional[list[Actor]]
    genre: Optional[list[str]]
    director: Optional[list[str]]


class SortEnum(Enum):
    id = "id"
    title = "title"
    imdb_rating = "imdb_rating"


class SortOrderEnum(Enum):
    asc = "asc"
    desc = "desc"
