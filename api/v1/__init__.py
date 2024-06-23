from fastapi import APIRouter
from .qr_endpoints import router as qr_router
from .finance.endpoints import router as stocks_router
from .other_endpoints import router as other_router
from .weather.endpoints import router as weather_router
from .geo.endpoints import router as geo_router
from .auth.endpoints import router as auth_router
from .sms_endpoints import router as sms_router
from .email_endpoints import router as email_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(email_router, prefix="/email")
v1_router.include_router(sms_router, prefix="/sms")
v1_router.include_router(qr_router, prefix="/qr")
v1_router.include_router(stocks_router, prefix="/finance")
v1_router.include_router(geo_router, prefix="/geo")
v1_router.include_router(weather_router, prefix="/weather")
v1_router.include_router(other_router, prefix="/other")