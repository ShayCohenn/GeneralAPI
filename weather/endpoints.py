from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from constants import DEFAULT_LIMITER, MAIN_ERROR_MESSAGE
from weather.methods import get_general_weather, get_current_temp
from rate_limit import limiter

router = APIRouter()

@router.get("/general")
@limiter.limit(DEFAULT_LIMITER)
def getGeneralWeather(request: Request, city: str, lang: str = "en"):
    try:
        response = get_general_weather(city, lang)
        if response == "404":
            return JSONResponse(content={"error": f"{city} was not found"}, status_code=404)
        elif not response:
            return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)
        else:
            return response
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)

@router.get("/current-temperature")
@limiter.limit(DEFAULT_LIMITER)
def getCurrentTemperature(request: Request, city: str, unit: str = "celsius"):
    try:
        response = get_current_temp(city, unit)
        if response == "404":
            return JSONResponse(content={"error": f"{city} was not found"}, status_code=404)
        elif not response:
            return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)
        else:
            return response
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)