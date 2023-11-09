from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from rate_limit import limiter
from QR.qr import router as qr_router
from finance.endpoints import router as stocks_router
from entertainment.endpoints import router as jokes_router
from weather.endpoints import router as weather_router
from sports.endpoints import router as sports_router

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Enable CORS for all origins 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
@limiter.limit("4/minute", key_func=get_remote_address)
async def test(request: Request):
    return {"msg":"test 4.0"}

app.include_router(qr_router, prefix="/qr")
app.include_router(stocks_router, prefix="/finance")
app.include_router(jokes_router, prefix="/entertainment")
app.include_router(weather_router, prefix="/weather")
app.include_router(sports_router, prefix="/sports")