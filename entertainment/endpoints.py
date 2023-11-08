import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from rate_limit import limiter

load_dotenv()

router = APIRouter()

dad_jokes_api = os.getenv("DAD_JOKES_API")
yo_momma_api = os.getenv("YO_MOMMA_API")
chuck_norris_api = os.getenv("CHUCK_NORRIS_API")
facts_api = os.getenv("FACTS_API")
riddles_api = os.getenv("RIDDLES_API")
emoji_api = os.getenv("EMOJI_API")

@router.get("/dad-joke")
@limiter.limit("1/second")
def dad_joke(request: Request):
    try:
        headers = {"Accept": "application/json"} 
        response = requests.get(dad_jokes_api, headers=headers) 

        if response.status_code == 200:
            joke_data = response.json()
            return {"joke":joke_data["joke"]}
        else:
            return {"error": "Failed to fetch a dad joke"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/yo-momma-joke")
@limiter.limit("1/second")
def yo_momma_joke(request: Request):
    try:
        response = requests.get(yo_momma_api)
        if(response.status_code == 200):
            joke_data = response.json()
            return joke_data
        else:
            return {"error": "Failed to fetch a yo momma joke"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/chuck-norris-joke")
@limiter.limit("1/second")
def chuck_norris_joke(request: Request):
    try:
        response = requests.get(chuck_norris_api)
        if(response.status_code == 200):
            joke_data = response.json()
            return {"joke":joke_data["value"]}
        else:
            return {"error": "Failed to fetch a chuck norris joke"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/random-fact")
@limiter.limit("1/second")
def random_fact(request: Request):
    try:
        response = requests.get(facts_api)
        if(response.status_code == 200):
            data = response.json()
            return {"fact": data["text"]}
        else:
            return {"error": "Failed to fetch a random fact"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/random-riddle")
@limiter.limit("1/second")
def random_riddle(request: Request):
    try:
        response = requests.get(riddles_api)
        if(response.status_code == 200):
            data = response.json()
            return data
        else:
            return {"error": "Failed to fetch a random riddle"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))