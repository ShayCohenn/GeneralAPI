from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from .functions import get_general_weather, get_current_temp

router = APIRouter()

@router.get("/general")
def general_weather(city: str, lang: str = "en"):
    response = get_general_weather(city, lang)
    return ORJSONResponse(content=response, status_code=200)

@router.get("/current-temperature")
def current_temperature(city: str, unit: str = "celsius"):
    response = get_current_temp(city, unit)
    return ORJSONResponse(content=response, status_code=200)