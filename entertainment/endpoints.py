import os
import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException

load_dotenv()

router = APIRouter()

dad_jokes_api = os.getenv("DAD_JOKES_API")
yo_momma_api = os.getenv("YO_MOMMA_API")
chuck_norris_api = os.getenv("CHUCK_NORRIS_API")
facts_api = os.getenv("FACTS_API")
riddles_api = os.getenv("RIDDLES_API")
emoji_api = os.getenv("EMOJI_API")

@router.get("/dad-joke")
def dad_joke():
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
def yo_momma_joke():
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
def chuck_norris_joke():
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
def random_fact():
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
def random_riddle():
    try:
        response = requests.get(riddles_api)
        if(response.status_code == 200):
            data = response.json()
            return data
        else:
            return {"error": "Failed to fetch a random riddle"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))