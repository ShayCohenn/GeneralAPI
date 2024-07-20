from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Setup:
    MONGODB_URI = getenv("MONGODB_URI")
    REDIS_URL = getenv('REDIS_URL')
    REDIS_PORT = int(getenv('REDIS_PORT'))
    REDIS_PASSWORD = getenv('REDIS_PASSWORD')
    GOOGLE_ID = getenv('GOOGLE_CLIENT_ID')
    GOOGLE_SECRET = getenv('GOOGLE_CLIENT_SECRET')
    SECRET_KEY = getenv('SECRET_KEY')
    ALGORITHM = getenv('ALGORITHM')

class EmailConfig:
    FROM_EMAIL = getenv('FROM_EMAIL')
    PASSWORD = getenv('PASSWORD')

class AppConfig:
    MODE = getenv('MODE')

# -------------------------------------------------------------------------- URLS -------------------------------------------------------------------

_LOCAL_URL = "127.0.0.1:8000"
_PRODUCTION_URL = "https://general-api.vercel.app/"

class URLS:
    API_URL = _PRODUCTION_URL if AppConfig.MODE == "production" else _LOCAL_URL
    FRONTEND_URL = "http://127.0.0.1:3000"
    GOOGLE_REDIRECT_URI = f"{FRONTEND_URL}/auth/google"