# ------------------------------------------------------------------- Environment Variables ---------------------------------------------------------

import os
from dotenv import load_dotenv

load_dotenv() 

DAD_JOKES_API = os.getenv("DAD_JOKES_API")
YO_MOMMA_API = os.getenv("YO_MOMMA_API")
CHUCK_NORRIS_API = os.getenv("CHUCK_NORRIS_API")
FACTS_API = os.getenv("FACTS_API")
RIDDLES_API = os.getenv("RIDDLES_API")

WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API")
WEATHER_API_URL = os.getenv("WEATHER_API_URL")

FOOTBALL_URL = os.getenv("FOOTBALL_WEBSITE_URL")

MONGODB_URI = os.getenv("MONGODB_URI")

SMS_SECRET = os.getenv('SMS_SECRET')
SMS_KEY = os.getenv('SMS_KEY')

FROM_EMAIL = os.getenv('FROM_EMAIL')
PASSWORD = os.getenv('PASSWORD')

MODE = os.getenv('MODE')

REDIS_URL = os.getenv('REDIS_URL')
REDIS_PORT = int(os.getenv('REDIS_PORT'))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

# -------------------------------------------------------------------------- URLS -------------------------------------------------------------------

LOCAL_URL = "127.0.0.1:8000"
PRODUCTION_URL = "https://general-api.vercel.app/"
CURRENT_URL = PRODUCTION_URL if MODE == "production" else LOCAL_URL

# ------------------------------------------------------------------- Messages ----------------------------------------------------------------------

MAIN_ERROR_MESSAGE = {"error":"an error has occured please try again later, if this error persists please contact 'shay91847@gmail.com'"}
MAIN_404_MESSAGE = {"error":"Could not find this endpoint. Visit our documentation website at /docs"}

# ------------------------------------------------------------------- MongoDB ----------------------------------------------------------------------

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
users_db = client['users']['users']
cities_collection = client['Locations']['Cities']
countries_collection = client['Locations']['Countries']

# ------------------------------------------------------------------- Functions ----------------------------------------------------------------
import re

def validate_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

# ------------------------------------------------------------------- Cache ----------------------------------------------------------------
from cachetools import LRUCache, TTLCache

cache = LRUCache(maxsize=2048)
timed_cache = TTLCache(ttl=120, maxsize=2048)

# ------------------------------------------------------------------- Redis ----------------------------------------------------------------
import redis

r = redis.Redis(
  host=REDIS_URL,
  port=REDIS_PORT,
  password=REDIS_PASSWORD)

# ------------------------------------------------------------------- Docs ----------------------------------------------------------------

VERSION = "0.0.2"

DESCRIPTION = """
# Welcome to GeneralAPI's documentation site.

GeneralAPI is an all purpose API built by the FastAPI framework.
GeneralAPI is very easy to use, just make a request to an endpoint of your choosing and get JSON in response.
In GeneralAPI you can get anything for your next project,
from financial data, generating QR codes, weather data, upcoming sports matches, email and sms sending services
and even random dad jokes, facts and riddles

## Usage:
All GeneralAPI's services are free to use, but the SMS and Email services require authentication and an API key,
Just register using the /auth/register endpoint and providing an email, username and a password.

Then all you need to do is to go to your email and click on the URL to verify you email and get your API key.

If you lost your API key just login to your account using your username and password and you'll get your API key

### Disclaimer:
As of version 0.0.2 you can only have 1 API key per account
"""