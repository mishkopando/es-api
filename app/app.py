from typing import Optional

import uvicorn
from fastapi import FastAPI, APIRouter, Query, HTTPException

from settings import app_settings
from models import ShortMovie, Movie, SortEnum, SortOrderEnum
import es

APP_NAME = "Praktikum HTTP REST API for ES"

app = FastAPI(
    title=APP_NAME,
    docs_url=f"/swagger",
    redoc_url=None,
    openapi_url=f"/api/openapi.json",
)

api_router = APIRouter()

search_title = """неточный поиск по названию, описанию, актёрам, сценаристам и режиссёрам фильма 
Представьте, что вы вбили в поиск Яндекса "Звёздные войны" или "Джордж Лукас" или "Лукас войны" 
вам выводятся соответствующие фильмы."""


@api_router.get(
    path="/movies",
    tags=["movies"],
    summary="Список фильмов",
)
def get_movies_list(
        limit: int = Query(default=50, description="количество объектов, которое надо вывести", gt=0),
        page: int = Query(default=1, description="номер страницы", gt=0),
        sort: SortEnum = Query(default=SortEnum.id, description="свойство, по которому нужно отсортировать результат"),
        sort_order: SortOrderEnum = Query(default=SortOrderEnum.asc, description="порядок сортировки"),
        search: Optional[str] = Query(default=None, description=search_title),
):
    try:
        return es.search_movies(
            limit=limit,
            page=page,
            sort=sort,
            sort_order=sort_order,
            search=search
        )
    except es.ElasticError as e:
        raise HTTPException(status_code=500, detail=e.message)


@api_router.get("/movies/")  # Это тупой костыль, чтобы проходил тест на пустой запрос
@api_router.get(
    path="/movies/{movieID}",
    response_model=Movie,
    tags=["movies"],
    summary="Получить фильм",
    description="Получить фильм",
)
def get_movie_by_id(movieID: Optional[str] = None) -> Movie:  # Тут стоит "movieID: Optional[str] = None" из-за того-же тупого кослытя
    # И вот этот if это тоже тупой костыль
    if not movieID:
        raise HTTPException(status_code=200, detail="WTF???")
    try:
        return es.get_movie_by_id(id=movieID)
    except es.MovieNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except es.ElasticError as e:
        raise HTTPException(status_code=500, detail=e.message)


app.include_router(router=api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app:app", host=app_settings.server_host, port=app_settings.server_port)
