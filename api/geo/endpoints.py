from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from .functions import query_cities, query_countries

router = APIRouter()

@router.get("/cities")
def cities(
    city: str = "",
    country: str = "",
    flag: bool = False,
    dial_code: bool = False,
    emoji: bool = False,
    country_code: bool = False,
    limit: int = 100
):
    cities = query_cities(city, country, flag, dial_code, emoji, country_code, limit)
    if len(cities) == 0:
        return ORJSONResponse(content={"error": "Couldn't find what you were looking for..."}, status_code=204)
    return ORJSONResponse(content=cities, status_code=200)

@router.get("/countries")
def countries(country: str = "", flag: bool = False, dial_code: bool = False, emoji: bool = False):
    items = query_countries(country, flag, dial_code, emoji)
    if len(items) == 0:
        return ORJSONResponse(content={"error": "Couldn't find what you were looking for..."}, status_code=204)
    return ORJSONResponse(content=items, status_code=200)

