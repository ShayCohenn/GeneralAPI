from fastapi.responses import ORJSONResponse
import requests
from fastapi import APIRouter, HTTPException
from constants import MAIN_ERROR_MESSAGE, DAD_JOKES_API, YO_MOMMA_API, CHUCK_NORRIS_API, FACTS_API, RIDDLES_API

router = APIRouter()

@router.get("/dad-joke")
def dad_joke() -> ORJSONResponse:
    try:
        headers = {"Accept": "application/json"} 
        response = requests.get(DAD_JOKES_API, headers=headers) 

        if response.status_code == 200:
            joke_data = response.json()
            return ORJSONResponse(content={"joke":joke_data["joke"]}, status_code=200)
        else:
            raise HTTPException(status_code=500, detail={"error":"could not fetch a random dad joke"})
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)

@router.get("/yo-momma-joke")
def yo_momma_joke() -> ORJSONResponse:
    try:
        response = requests.get(YO_MOMMA_API)
        if(response.status_code == 200):
            joke_data = response.json()
            return ORJSONResponse(content=joke_data, status_code=200)
        else:
            raise HTTPException(status_code=500, detail={"error":"could not fetch a random yo momma joke"})
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)
    
@router.get("/chuck-norris-joke")
def chuck_norris_joke() -> ORJSONResponse:
    try:
        response = requests.get(CHUCK_NORRIS_API)
        if(response.status_code == 200):
            joke_data = response.json()
            return ORJSONResponse(content={"joke":joke_data["value"]}, status_code=200)
        else:
            raise HTTPException(status_code=500, detail={"error":"could not fetch a random chuck norris joke"})
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)

@router.get("/random-fact")
def random_fact() -> ORJSONResponse:
    try:
        response = requests.get(FACTS_API)
        if(response.status_code == 200):
            data = response.json()
            return ORJSONResponse(content={"fact": data["text"]}, status_code=200)
        else:
            raise HTTPException(status_code=500, detail={"error":"could not fetch a random fact"})
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)
    
@router.get("/random-riddle")
def random_riddle() -> ORJSONResponse:
    try:
        response = requests.get(RIDDLES_API)
        if(response.status_code == 200):
            data = response.json()
            return ORJSONResponse(content=data, status_code=200)
        else:
            raise HTTPException(status_code=500, detail={"error":"could not fetch a random riddle"})
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)