"""Тут будут медоты обращения в элестику."""
from typing import Optional
import json as j

import httpx
from httpx import RequestError

from settings import app_settings
from models import Movie, ShortMovie, SortEnum, SortOrderEnum


def movies_search(json):
    try:
        resp = httpx.request(
            method="GET",
            url=f"{app_settings.elastic_url}/movies/_search",
            json=json,
        )
    except RequestError:
        raise ElasticError
    return resp.json()


def get_movie_by_id(id: str) -> Movie:
    """Возвращает фильм по его id."""
    json = {"query": {"match": {"id": id}}}
    resp = movies_search(json=json)
    movies_count = resp["hits"]["total"]["value"]

    if movies_count == 0:
        raise MovieNotFoundException
    elif movies_count > 1:
        raise TooMuchMoviesFoundException(id=id, count=movies_count)
    else:
        movie = resp["hits"]["hits"][0]["_source"]
        return Movie.parse_obj(movie)


def search_movies(
        limit: int,
        page: int,
        sort: SortEnum,
        sort_order: SortOrderEnum,
        search: Optional[str]
) -> list[ShortMovie]:
    """Поиск фильмов по параметрам."""
    json = {
        "from": (page - 1) * limit,
        "size": limit,
        "sort": [
            {
                f"{sort.value}.raw" if sort == SortEnum.title else sort.value: {
                    "order": sort_order.value
                }
            }
        ]
    }
    if search:
        json["query"] = {
            "multi_match": {
                "query": search,
                "fuzziness": "auto",
                "fields": [
                    "title^5",
                    "description^4",
                    "actors_names^3",
                    "writers_names^2",
                    "director"
                ]
            }
        }
    resp = movies_search(json=json)
    movies_count = len(resp["hits"]["hits"])
    if movies_count > 0:
        return [ShortMovie.parse_obj(item["_source"]) for item in resp["hits"]["hits"]]
    else:
        return []


class MovieNotFoundException(Exception):
    def __init__(self):
        self.message = "Фильм не найден"


class TooMuchMoviesFoundException(Exception):
    def __init__(self, id: str, count: int):
        self.message = f"Found {count} movies by ID: {id}"


class ElasticError(Exception):
    def __init__(self):
        self.message = "Elastic have some problems..."
