from fastapi import HTTPException
from cachetools import cached
from core.utils import cache, validate_input
from core.db import cities_collection, countries_collection
from .models import City, Country

top11_cities = [
    {"city":"New York City","country":"United States"}, 
    {"city":"Rome","country":"Italy"}, 
    {"city":"Tel Aviv","country":"Israel"},
    {"city":"London","country":"United Kingdom"}, 
    {"city":"São Paulo","country":"Brazil"}, 
    {"city":"Lod","country":"Israel"}, 
    {"city":"Paris","country":"France"}, 
    {"city":"Tokyo","country":"Japan"},
    {"city":"Beijing","country":"China"}, 
    {"city":"Osaka","country":"Japan"}
    ]

@cached(cache)
def query_cities(
    city: str = "",
    country: str = "",
    flag: bool = False,
    dial_code: bool = False,
    emoji: bool = False,
    limit: int = 100) -> list[City]:

    if city and not validate_input(city):
        raise HTTPException(detail={"error":"Invalid city name"}, status_code=400)
    if country and not validate_input(country):
        raise HTTPException(detail={"error":"Invalid country name"}, status_code=400)

    query = {}

    # Add city filter if specified
    if city:
        query["name"] = {"$regex": f'^{city}', "$options": 'i'}

    # Add country filter if specified
    if country:
        query["country"] = {"$regex": f'^{country}', "$options": 'i'}

    if not query:  # If no filters are specified, return the top results
        top_cities_query = {"$or": [{"name": city_data["city"], "country": city_data["country"]} for city_data in top11_cities]}
        top_cities_results = list(cities_collection.find(top_cities_query).sort([("name", 1)]))
        results: list[dict] = top_cities_results
    else:
        # Sort by population in descending order and then by name
        results: list[dict] = list(cities_collection.find(query).sort([("population", -1), ("name", 1)]))

    # Collect unique country names
    country_names: set[dict] = set(result.get("country") for result in results if result.get("country"))

    # Fetch country details for all unique country names in a single query
    country_details_query = {"name": {"$in": list(country_names)}}
    country_details_cursor: list[dict] = countries_collection.find(country_details_query)

    # Create a dictionary for efficient lookup of country details based on country names
    country_details_dict = {country.get("name"): country for country in country_details_cursor}

    items = []
    exact_match_items = []  # To store all items with an exact name match

    for result in results:
        city_name: str = result.get("name")
        country_name: str = result.get("country") 

        # Get country details from the dictionary
        country_details = country_details_dict.get(country_name, {})

        item = dict(City(
            city=city_name,
            country=country_name,
            flag=country_details.get("image") if flag else None,
            dial_code=country_details.get("dial_code") if dial_code else None,
            emoji=country_details.get("emoji") if emoji else None,
        ))

        if city_name.lower() == city.lower():
            # If city_name is an exact match, add it to the list
            exact_match_items.append(item)
        else:
            items.append(item)

    # Add up to 'limit' exact match items at the beginning of the items array
    items = exact_match_items + items

    return items[:limit]

@cached(cache)
def query_countries(country: str = "", flag: bool = False, dial_code: bool = False, emoji: bool = False) -> list[Country]:
    if country and not validate_input(country):
        raise HTTPException(detail={"error":"Invalid country name"}, status_code=400)
    
    query = {"name": {"$regex": f'^{country}', "$options": 'i'}}

    results: list[dict] = list(countries_collection.find(query).sort("name", 1))

    items = []
    for result in results:
        country_name = result.get("name")

        item = dict(Country(
            country=country_name,
            flag=result.get("image") if flag else None,
            dial_code=result.get("dial_code") if dial_code else None,
            emoji=result.get("emoji") if emoji else None
        ))

        items.append(item)

    return items