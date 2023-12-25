from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from constants import MAIN_404_MESSAGE
from rate_limit import limiter
from QR.qr import router as qr_router
from finance.endpoints import router as stocks_router
from entertainment.endpoints import router as jokes_router
from weather.endpoints import router as weather_router
from sports.endpoints import router as sports_router
from data.endpoints import router as data_router

# ----------------------------------------------- App Initialization ----------------------------------------------------------------------

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

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
app.include_router(jokes_router, prefix="/entertainment")
app.include_router(weather_router, prefix="/weather")
app.include_router(sports_router, prefix="/sports")
app.include_router(data_router, prefix="/data")