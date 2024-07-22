from os import getenv
from dotenv import load_dotenv

load_dotenv()

class DBConfig:
    MONGODB_URI: str = getenv("MONGODB_URI")

class RedisConfig:    
    REDIS_URL: str = getenv('REDIS_URL')
    REDIS_PORT: int = int(getenv('REDIS_PORT'))
    REDIS_PASSWORD: str = getenv('REDIS_PASSWORD')

class GoogleConfig:
    GOOGLE_ID: str = getenv('GOOGLE_CLIENT_ID')
    GOOGLE_SECRET: str = getenv('GOOGLE_CLIENT_SECRET')

class Secrets:
    SECRET_KEY: str = getenv('SECRET_KEY')
    ALGORITHM: str = getenv('ALGORITHM')

class EmailConfig:
    FROM_EMAIL: str = getenv('FROM_EMAIL')
    PASSWORD: str = getenv('PASSWORD')

class AppConfig:
    MODE: str = getenv('MODE')

# -------------------------------------------------------------------------- URLS -------------------------------------------------------------------

_FRONTEND_LOCAL_URL = ["http://localhost:3000", "http://127.0.0.1:3000"]
_FRONTEND_PRODUCTION_URL = ["https://general-api.vercel.app"]

class URLS:
    FRONTEND_URL: str = _FRONTEND_PRODUCTION_URL if AppConfig.MODE == "production" else _FRONTEND_LOCAL_URL
    GOOGLE_REDIRECT_URI: str = f"{FRONTEND_URL}/auth/google"
    GOOOGLE_LOGIN_URL: str = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GoogleConfig.GOOGLE_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"

class Messages:
    MAIN_ERROR_MESSAGE: str = {"error":"an error has occured please try again later, if this error persists please contact 'shay91847@gmail.com'"}
    MAIN_404_MESSAGE: str = {"error":"Could not find this endpoint."}
    ACCOUNT_VERIFY_EMAIL_MESSAGE: str = f"Please verify your account by clicking on the following link: {URLS.FRONTEND_URL}/activation/"
    CHANGE_PASSWORD_EMAIL_MESSAGE: str = f"Please reset your password by clicking on the following link: {URLS.FRONTEND_URL}/confirm-reset-password/"