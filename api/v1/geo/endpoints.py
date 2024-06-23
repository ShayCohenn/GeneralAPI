from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from .functions import query_cities, query_countries
from .models import City, Country

router = APIRouter()

@router.get("/cities")
def cities(
    city: str = "",
    country: str = "",
    flag: bool = False,
    dial_code: bool = False,
    emoji: bool = False,
    limit: int = 100
) -> ORJSONResponse:
    items: list[City] = query_cities(city, country, flag, dial_code, emoji, limit)
    if len(items) == 0:
        raise HTTPException(status_code=204)
    return ORJSONResponse(content=items, status_code=200)

@router.get("/countries")
def countries(country: str = "", flag: bool = False, dial_code: bool = False, emoji: bool = False) -> ORJSONResponse:
    items: list[Country] = query_countries(country, flag, dial_code, emoji)
    if len(items) == 0:
        raise HTTPException(status_code=204)
    return ORJSONResponse(content=items, status_code=200)