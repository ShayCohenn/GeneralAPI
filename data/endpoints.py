from fastapi import APIRouter, Request
from constants import DEFAULT_LIMITER, MONGODB_URI
from rate_limit import limiter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

router = APIRouter()


# Create a new client and connect to the server
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))

locations_db = client["Locations"]
cities_collection = locations_db['Cities']
countries_collection = locations_db['Countries']

top11_cities = [
    {"city":"Tokyo","country":"Japan"}, 
    {"city":"Delhi","country":"India"}, 
    {"city":"Shanghai","country":"China"}, 
    {"city":"São Paulo","country":"Brazil"}, 
    {"city":"Mexico City","country":"Mexico"}, 
    {"city":"Mumbai","country":"India"}, 
    {"city":"Beijing","country":"China"}, 
    {"city":"Dhaka","country":"Bangladesh"}, 
    {"city":"Osaka","country":"Japan"}, 
    {"city":"New York City","country":"United States"}, 
    ]

@router.get("/cities")
@limiter.limit(DEFAULT_LIMITER)
def cities(request: Request, city: str = "", country: str = "", flag: bool = False, dial_code: bool = False, emoji: bool = False):
    # Example query: find all documents in the collection
    query = {}
    
    # Add city filter if specified
    if city:
        query["name"] = {"$regex": f'^{city}', "$options": 'i'}
    
    # Add country filter if specified
    if country:
        query["country"] = {"$regex": f'^{country}', "$options": 'i'}

    if not query:  # If no filters are specified, return the top 11 results
        top_cities_query = {"$or": [{"name": city_data["city"], "country": city_data["country"]} for city_data in top11_cities]}
        top_cities_results = list(cities_collection.find(top_cities_query).sort([("name", 1)]).limit(11))
        results = top_cities_results
    else:
        results = list(cities_collection.find(query).sort([("name", 1)]))


    # Collect unique country names
    country_names = set(result.get("country") for result in results if result.get("country"))

    # Fetch country details for all unique country names in a single query
    country_details_query = {"name": {"$in": list(country_names)}}
    country_details_cursor = countries_collection.find(country_details_query)

    # Create a dictionary for efficient lookup of country details based on country names
    country_details_dict = {country.get("name"): country for country in country_details_cursor}

    # Sort the results by length of "name" field
    results.sort(key=lambda x: len(x["name"]))

    items = []
    for result in results:
        city_name = result.get("name")
        country_name = result.get("country")
        
        # Get country details from the dictionary
        country_details = country_details_dict.get(country_name, {})
        
        item = {
            "city": city_name,
            "country":country_name,
        }
        if flag:
            flag_image = country_details.get("image", None)
            item["flag"] = flag_image
            
        if dial_code:
            code = country_details.get("dial_code", None)
            item["dial_code"] = code

        if emoji:
            emj = country_details.get("emoji", None)
            item["emoji"] = emj

        items.append(item)

    if len(items) == 0:
        return {"error": "Couldn't find what you were looking for..."}
    return items

@router.get("/countries")
@limiter.limit(DEFAULT_LIMITER)
def countries(request: Request, country: str = "", flag: bool = False, phone_code: bool = False, emoji: bool = False):
    # Example query: find all documents in the collection
    query = {"name": {"$regex": f'^{country}', "$options": 'i'}}

    results = list(countries_collection.find(query).sort([("name", 1)]))
    results.sort(key=lambda x: len(x["name"]))

    items = []
    for result in results:
        country_name = result.get("name")

        item = {
            "country": country_name,
        }
        if flag:
            flag_image = result.get("image", None)
            item["flag"] = flag_image
        if phone_code:
            dial_code = result.get("dial_code", None)
            item["phone_code"] = dial_code
        if emoji:
            country_emoji = result.get("emoji", None)
            item["emoji"] = country_emoji

        items.append(item)

    if len(items) == 0:
        return {"error": "Couldn't find what you were looking for..."}
    return items

