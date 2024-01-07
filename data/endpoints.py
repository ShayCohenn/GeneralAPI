from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from constants import DEFAULT_LIMITER, MONGODB_URI
from rate_limit import limiter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

router = APIRouter()

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

@router.get("/cities")
def cities(request: Request, city: str, country: str = ""):
    db = client["Locations"]
    collection = db['Cities']
    # Example query: find all documents in the collection
    query = {"name": {"$regex": f'^{city}', "$options": 'i'}}
    
    # Add country filter if specified
    if country:
        query["country"] = {"$regex": country, "$options": 'i'}

    results = list(collection.find(query).sort([("name", 1)]))
    results.sort(key=lambda x: len(x["name"]))

    items = [{"city": result.get("name"), "country": result.get("country")} for result in results]
    if len(items) == 0:
        return {"error":"Couldn't find what you were looking for..."}
    return items

