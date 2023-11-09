from fastapi import APIRouter, HTTPException, Request
import yfinance as yf
from rate_limit import limiter, DEFAULT_LIMITER

router = APIRouter()

class TickerNotFoundError(HTTPException):
    def __init__(self, ticker: str):
        detail = f"Ticker {ticker} not found."
        super().__init__(status_code=404, detail=detail)

def verify_ticker(ticker: str):
    data = yf.Ticker(ticker)
    if not data.history(period="1d").empty:
        return data
    raise TickerNotFoundError(ticker)

@router.get("/general-info")
@limiter.limit(DEFAULT_LIMITER)
def get_info(request: Request, ticker: str):
    try:
        data = verify_ticker(ticker)
        return data.info
    except TickerNotFoundError as e:
        raise e

@router.get("/current-value")
@limiter.limit(DEFAULT_LIMITER)
def get_value(request: Request, ticker: str):
    try:
        data = verify_ticker(ticker)
        current_price = data.history(period="1d")['Close'].iloc[-1]
        return {"current_value": current_price}
    except TickerNotFoundError as e:
        raise e
    
@router.get("/currency-convert")
@limiter.limit(DEFAULT_LIMITER)
def get_exchange_rate(request: Request, from_curr: str, to_curr: str, amount: float = 1):
    try:
        data = verify_ticker(f'{from_curr}{to_curr}=X')
        result = data.history(period="1d")["Close"].iloc[-1] * amount
        return {"result":result}
    except TickerNotFoundError as e:
        raise e
