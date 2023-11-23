
# ------------------------------------------------------------------- Environment Variables ---------------------------------------------------------

import os
from dotenv import load_dotenv

load_dotenv() 

DAD_JOKES_API = os.getenv("DAD_JOKES_API")
YO_MOMMA_API = os.getenv("YO_MOMMA_API")
CHUCK_NORRIS_API = os.getenv("CHUCK_NORRIS_API")
FACTS_API = os.getenv("FACTS_API")
RIDDLES_API = os.getenv("RIDDLES_API")

WEATHER_API = os.getenv("OPEN_WEATHER_API")
WEATHER_API_URL = f"https://api.openweathermap.org/data/2.5/weather?appid={WEATHER_API}"

FOOTBALL_URL = os.getenv("FOOTBALL_WEBSITE_URL")

# ------------------------------------------------------------------- Messages ----------------------------------------------------------------------

MAIN_ERROR_MESSAGE = {"error":"an error has occured please try again later, if this error persists please contact 'shay91847@gmail.com'"}

# ------------------------------------------------------------------- Limiters ----------------------------------------------------------------------

DEFAULT_LIMITER = "1/second"
SMALL_LIMITER = "2/second"
LARGE_LIMITER = "1 per 2 seconds; 10 per minute"