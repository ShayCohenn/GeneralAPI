import requests
from fastapi.responses import ORJSONResponse
from fastapi import APIRouter, HTTPException
from core.config import APIConfig

router = APIRouter()

@router.get("/dad-joke")
def dad_joke() -> ORJSONResponse:
    headers = {"Accept": "application/json"} 
    response = requests.get(APIConfig.DAD_JOKES_API, headers=headers) 

    if response.status_code == 200:
        joke_data = response.json()
        return ORJSONResponse(content={"joke":joke_data["joke"]}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail={"error":"could not fetch a random dad joke"})

@router.get("/yo-momma-joke")
def yo_momma_joke() -> ORJSONResponse:
    response = requests.get(APIConfig.YO_MOMMA_API)
    if(response.status_code == 200):
        joke_data = response.json()
        return ORJSONResponse(content=joke_data, status_code=200)
    else:
        raise HTTPException(status_code=500, detail={"error":"could not fetch a random yo momma joke"})
    
@router.get("/chuck-norris-joke")
def chuck_norris_joke() -> ORJSONResponse:
    response = requests.get(APIConfig.CHUCK_NORRIS_API)
    if(response.status_code == 200):
        joke_data = response.json()
        return ORJSONResponse(content={"joke":joke_data["value"]}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail={"error":"could not fetch a random chuck norris joke"})

@router.get("/random-fact")
def random_fact() -> ORJSONResponse:
    response = requests.get(APIConfig.FACTS_API)
    if(response.status_code == 200):
        data = response.json()
        return ORJSONResponse(content={"fact": data["text"]}, status_code=200)
    else:
        raise HTTPException(status_code=500, detail={"error":"could not fetch a random fact"})
    
@router.get("/random-riddle")
def random_riddle() -> ORJSONResponse:
    response = requests.get(APIConfig.RIDDLES_API)
    if(response.status_code == 200):
        data = response.json()
        return ORJSONResponse(content=data, status_code=200)
    else:
        raise HTTPException(status_code=500, detail={"error":"could not fetch a random riddle"})