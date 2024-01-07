from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from constants import DEFAULT_LIMITER, MONGODB_URI
from rate_limit import limiter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

router = APIRouter()

# Create a new client and connect to the server
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

db = client["sample_airbnb"]
collection = db['listingsAndReviews']

@router.get("/test")
@limiter.limit(DEFAULT_LIMITER)
def test(request: Request):
    # Example query: find all documents in the collection
    result = collection.find({"beds":5})
    # Convert the result to a list (if needed) and return it
    docs = list(result)
    items = [{"_id": doc.get("_id"), "space": doc.get("space")} for doc in docs]
    return {"test":items[0]}

