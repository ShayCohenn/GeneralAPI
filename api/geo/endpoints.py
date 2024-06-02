from fastapi import APIRouter
from constants import cities_collection, countries_collection

router = APIRouter()

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
def cities(
    city: str = "",
    country: str = "",
    flag: bool = False,
    dial_code: bool = False,
    emoji: bool = False,
    country_code: bool = False,
    limit: int = 200000
):
    # Example query: find all documents in the collection
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
        results = top_cities_results
    else:
        # Sort by population in descending order and then by name
        results = list(cities_collection.find(query).sort([("population", -1), ("name", 1)]))

    # Collect unique country names
    country_names = set(result.get("country") for result in results if result.get("country"))

    # Fetch country details for all unique country names in a single query
    country_details_query = {"name": {"$in": list(country_names)}}
    country_details_cursor = countries_collection.find(country_details_query)

    # Create a dictionary for efficient lookup of country details based on country names
    country_details_dict = {country.get("name"): country for country in country_details_cursor}

    items = []
    exact_match_items = []  # To store all items with an exact name match

    for result in results:
        city_name: str = result.get("name")
        country_name: str = result.get("country")

        # Get country details from the dictionary
        country_details = country_details_dict.get(country_name, {})

        item = {
            "city": city_name,
            "country": country_name,
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
        if country_code:
            code = country_details.get("code", None)
            item["country_code"] = code

        if city_name.lower() == city.lower():
            # If city_name is an exact match, add it to the list
            exact_match_items.append(item)
        else:
            items.append(item)

    # Add up to 'limit' exact match items at the beginning of the items array
    items = exact_match_items + items

    if len(items) == 0:
        return {"error": "Couldn't find what you were looking for..."}
    return items[:limit]

@router.get("/countries")
def countries(country: str = "", flag: bool = False, dial_code: bool = False, emoji: bool = False):
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
        if dial_code:
            code = result.get("dial_code", None)
            item["dial_code"] = code
        if emoji:
            country_emoji = result.get("emoji", None)
            item["emoji"] = country_emoji

        items.append(item)

    if len(items) == 0:
        return {"error": "Couldn't find what you were looking for..."}
    return items

