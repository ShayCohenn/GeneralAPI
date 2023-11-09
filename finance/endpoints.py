from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import yfinance as yf
from rate_limit import limiter
from constants import DEFAULT_LIMITER, MAIN_ERROR_MESSAGE

router = APIRouter()

def verify_ticker(ticker: str):
    data = yf.Ticker(ticker)
    if not data.history(period="1d").empty:
        return data
    return None

@router.get("/current-value")
@limiter.limit(DEFAULT_LIMITER)
def get_value(request: Request, ticker: str):
    try:
        data = verify_ticker(ticker)
        if data:
            current_price = data.history(period="1d")['Close'].iloc[-1]
            return {"current_value": current_price}
        return JSONResponse(status_code=404, content={"error":f"could not find stock symbol {ticker}"})
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)
    
@router.get("/currency-convert")
@limiter.limit(DEFAULT_LIMITER)
def get_exchange_rate(request: Request, from_curr: str, to_curr: str, amount: float = 1):
    try:
        data = verify_ticker(f'{from_curr}{to_curr}=X')
        if data:
            result = data.history(period="1d")["Close"].iloc[-1] * amount
            return {"result":result}
        return JSONResponse(status_code=404, content={"error":f"could not find exchange rate for {from_curr}/{to_curr}"})
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)