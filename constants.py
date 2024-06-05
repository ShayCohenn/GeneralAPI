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

SECRET = os.getenv('SMS_SECRET')
SMS_KEY = os.getenv('SMS_KEY')

FROM_EMAIL = os.getenv('FROM_EMAIL')
PASSWORD = os.getenv('PASSWORD')

MODE = os.getenv('MODE')

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

# ------------------------------------------------------------------- Docs ----------------------------------------------------------------

VERSION = "0.0.2"

DESCRIPTION = """
## Email
send emails

## SMS 
send sms
"""

SUMMARY = """GeneralAPI is a microservice API that handles every task for your app, from generatign QR codes, to
 gettign financial and weather data and sending emails and sms"""