from fastapi import APIRouter, HTTPException, Request
from weather.methods import get_general_weather, get_current_temp
from rate_limit import limiter

router = APIRouter()

@router.get("/general")
@limiter.limit("1/second")
def getGeneralWeather(request: Request, city: str, lang: str = "en"):
    try:
        return get_general_weather(city, lang)
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))

@router.get("/current-temperature")
@limiter.limit("1/second")
def getCurrentTemperature(request: Request, city: str, unit: str = "celsius"):
    try:
        return get_current_temp(city, unit)
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))