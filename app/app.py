from typing import Optional

import uvicorn
from fastapi import FastAPI, APIRouter, Query

from settings import Settings
from models import ShortMovie, Movie, SortEnum, SortOrderEnum


APP_NAME = "Praktikum HTTP REST API for ES"

app = FastAPI(
    title=APP_NAME,
    docs_url=f"/swagger",
    redoc_url=None,
    openapi_url=f"/api/openapi.json",
)

api_router = APIRouter()
app_settings = Settings()

search_title = """неточный поиск по названию, описанию, актёрам, сценаристам и режиссёрам фильма 
Представьте, что вы вбили в поиск Яндекса "Звёздные войны" или "Джордж Лукас" или "Лукас войны" 
вам выводятся соответствующие фильмы."""


@api_router.get(
    path="/movies",
    tags=["movies"],
    summary="Список фильмов",
)
async def get_movies_list(
        limit: int = Query(default=50, description="количество объектов, которое надо вывести", gt=0),
        page: int = Query(default=1, description="номер страницы", gt=0),
        sort: SortEnum = Query(default=SortEnum.id, description="свойство, по которому нужно отсортировать результат"),
        sort_order: SortOrderEnum = Query(default=SortOrderEnum.asc, description="порядок сортировки"),
        search: Optional[str] = Query(default=None, description=search_title),
):
    return {
        "limit": limit,
        "page": page,
        "sort": sort,
        "sort_order": sort_order,
        "search": search
    }


@api_router.get(
    path="/movies/{movieID}",
    tags=["movies"],
    summary="Получить фильм",
    description="Получить фильм",
)
async def get_movie_by_id(movieID: str):
    return {"movie_id": movieID}

app.include_router(router=api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app:app", host=app_settings.server_host, port=app_settings.server_port)
