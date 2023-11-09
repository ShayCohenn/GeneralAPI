from fastapi.responses import JSONResponse
import requests
from fastapi import APIRouter, Request
from constants import DEFAULT_LIMITER, MAIN_ERROR_MESSAGE, DAD_JOKES_API, YO_MOMMA_API, CHUCK_NORRIS_API, FACTS_API, RIDDLES_API
from rate_limit import limiter

router = APIRouter()

@router.get("/dad-joke")
@limiter.limit(DEFAULT_LIMITER)
def dad_joke(request: Request):
    try:
        headers = {"Accept": "application/json"} 
        response = requests.get(DAD_JOKES_API, headers=headers) 

        if response.status_code == 200:
            joke_data = response.json()
            return {"joke":joke_data["joke"]}
        else:
            return JSONResponse(status_code=500, content={"error":"could not fetch a random dad joke"})
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)

@router.get("/yo-momma-joke")
@limiter.limit(DEFAULT_LIMITER)
def yo_momma_joke(request: Request):
    try:
        response = requests.get(YO_MOMMA_API)
        if(response.status_code == 200):
            joke_data = response.json()
            return joke_data
        else:
            return JSONResponse(status_code=500, content={"error":"could not fetch a random yo momma joke"})
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)
    
@router.get("/chuck-norris-joke")
@limiter.limit(DEFAULT_LIMITER)
def chuck_norris_joke(request: Request):
    try:
        response = requests.get(CHUCK_NORRIS_API)
        if(response.status_code == 200):
            joke_data = response.json()
            return {"joke":joke_data["value"]}
        else:
            return JSONResponse(status_code=500, content={"error":"could not fetch a random chuck norris joke"})
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)

@router.get("/random-fact")
@limiter.limit(DEFAULT_LIMITER)
def random_fact(request: Request):
    try:
        response = requests.get(FACTS_API)
        if(response.status_code == 200):
            data = response.json()
            return {"fact": data["text"]}
        else:
            return JSONResponse(status_code=500, content={"error":"could not fetch a random fact"})
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)
    
@router.get("/random-riddle")
@limiter.limit(DEFAULT_LIMITER)
def random_riddle(request: Request):
    try:
        response = requests.get(RIDDLES_API)
        if(response.status_code == 200):
            data = response.json()
            return data
        else:
            return JSONResponse(status_code=500, content={"error":"could not fetch a random riddle"})
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)