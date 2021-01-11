"""Тут будут медоты обращения в элестику."""
import httpx
from httpx import RequestError

from settings import app_settings
from models import Movie


def get_movie_by_id(id: str) -> Movie:
    """Возвращает фильм по его id."""
    json = {
                "query": {
                    "match": {
                        "id": id
                    }
                }
            }
    try:
        resp = httpx.request(
            method="GET",
            url=f"{app_settings.elastic_url}/movies/_search",
            json=json,
        )
    except RequestError:
        raise ElasticError

    json_resp = resp.json()
    movies_count = json_resp["hits"]["total"]["value"]

    if movies_count == 0:
        raise MovieNotFoundException
    elif movies_count > 1:
        raise TooMuchMoviesFoundException(id=id, count=movies_count)
    else:
        movie = json_resp["hits"]["hits"][0]["_source"]
        return Movie.parse_obj(movie)


class MovieNotFoundException(Exception):
    def __init__(self):
        self.message = "Фильм не найден"


class TooMuchMoviesFoundException(Exception):
    def __init__(self, id: str, count: int):
        self.message = f"Found {count} movies by ID: {id}"


class ElasticError(Exception):
    def __init__(self):
        self.message = "Elastic have some problems..."
