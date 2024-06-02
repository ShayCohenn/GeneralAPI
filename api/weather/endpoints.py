from fastapi import APIRouter
from fastapi.responses import JSONResponse
from constants import MAIN_ERROR_MESSAGE
from .methods import get_general_weather, get_current_temp

router = APIRouter()

@router.get("/general")
def getGeneralWeather(city: str, lang: str = "en"):
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
def getCurrentTemperature(city: str, unit: str = "celsius"):
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