from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from constants import MAIN_ERROR_MESSAGE
from .functions import get_general_weather, get_current_temp

router = APIRouter()

@router.get("/general")
def getGeneralWeather(city: str, lang: str = "en"):
    try:
        response = get_general_weather(city, lang)
        if response == "404":
            raise HTTPException(detail={"error": f"{city} was not found"}, status_code=202)
        elif not response:
            raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)
        else:
            return ORJSONResponse(content=response, status_code=200)
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)

@router.get("/current-temperature")
def getCurrentTemperature(city: str, unit: str = "celsius"):
    try:
        response = get_current_temp(city, unit)
        if response == "404":
            raise HTTPException(detail={"error": f"{city} was not found"}, status_code=202)
        elif not response:
            raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)
        else:
            return ORJSONResponse(content=response, status_code=200)
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)