from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from constants import MAIN_404_MESSAGE, SUMMARY, VERSION, DESCRIPTION
from api.QR.qr import router as qr_router
from api.finance.endpoints import router as stocks_router
from api.other.endpoints import router as other_router
from api.weather.endpoints import router as weather_router
from api.sports.endpoints import router as sports_router
from api.geo.endpoints import router as geo_router
from api.auth.endpoints import router as auth_router
from api.sms.endpoints import router as sms_router
from api.email.endpoints import router as email_router

# ----------------------------------------------- App Initialization ----------------------------------------------------------------------

app = FastAPI(title="GeneralAPI",description=DESCRIPTION, version=VERSION, summary=SUMMARY)

# ----------------------------------------------- Enable CORS for all origins -------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(404)
async def custom_404_handler(_, __):
    return JSONResponse(status_code=404, content=MAIN_404_MESSAGE)

# ----------------------------------------------- Including The Routers -------------------------------------------------------------------

app.include_router(qr_router, prefix="/qr")
app.include_router(stocks_router, prefix="/finance")
app.include_router(other_router, prefix="/other")
app.include_router(weather_router, prefix="/weather")
app.include_router(sports_router, prefix="/sports")
app.include_router(geo_router, prefix="/geo")
app.include_router(auth_router, prefix="/auth")
app.include_router(sms_router, prefix="/sms")
app.include_router(email_router, prefix="/email")