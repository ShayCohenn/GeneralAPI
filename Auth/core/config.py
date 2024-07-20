from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Setup:
    MONGODB_URI: str = getenv("MONGODB_URI")
    REDIS_URL: str = getenv('REDIS_URL')
    REDIS_PORT: int = int(getenv('REDIS_PORT'))
    REDIS_PASSWORD: str = getenv('REDIS_PASSWORD')
    GOOGLE_ID: str = getenv('GOOGLE_CLIENT_ID')
    GOOGLE_SECRET: str = getenv('GOOGLE_CLIENT_SECRET')
    SECRET_KEY: str = getenv('SECRET_KEY')
    ALGORITHM: str = getenv('ALGORITHM')

class EmailConfig:
    FROM_EMAIL: str = getenv('FROM_EMAIL')
    PASSWORD: str = getenv('PASSWORD')

class AppConfig:
    MODE: str = getenv('MODE')

class Messages:
    MAIN_ERROR_MESSAGE: str = {"error":"an error has occured please try again later, if this error persists please contact 'shay91847@gmail.com'"}
    MAIN_404_MESSAGE: str = {"error":"Could not find this endpoint. Visit our documentation website at /docs"}

# -------------------------------------------------------------------------- URLS -------------------------------------------------------------------

_FRONTEND_LOCAL_URL = "http://127.0.0.1:3000"
_FRONTEND_PRODUCTION_URL = "https://general-api.vercel.app/"

class URLS:
    FRONTEND_URL: str = _FRONTEND_PRODUCTION_URL if AppConfig.MODE == "production" else _FRONTEND_LOCAL_URL
    GOOGLE_REDIRECT_URI: str = f"{FRONTEND_URL}/auth/google"