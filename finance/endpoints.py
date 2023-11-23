from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import yfinance as yf
from rate_limit import limiter
from constants import DEFAULT_LIMITER, LARGE_LIMITER, MAIN_ERROR_MESSAGE
from datetime import datetime
import pandas as pd

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
    
@router.get("/stock-data")
@limiter.limit(LARGE_LIMITER)
async def get_stock_data(request: Request, ticker: str, start:str, end:str):
    try:
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d')
        except:
            return JSONResponse(status_code=400, content={"error":"invalid start date format"})
        try:
            end_date = datetime.now() if end.lower() in {"today","now"} else datetime.strptime(end, '%Y-%m-%d')
        except:
            return JSONResponse(status_code=400, content={"error":"invalid end date format"})
        if start_date >= end_date:
            return JSONResponse(status_code=400, content={"error":"start date cannot be the same or after end date"})
        if start_date > datetime.now() or end_date > datetime.now():
            return JSONResponse(status_code=400, content={"error":"cannot get stock data from the future"})
        verified_ticker = verify_ticker(ticker)
        if not verified_ticker:
            return JSONResponse(status_code=400, content={"error":f"could not find stock symbol {ticker}"})
        data = yf.download(ticker, start=start_date, end=end_date)
        data = data.reset_index()
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date'] = data['Date'].dt.date
        stock_data = data.to_dict(orient='records')
        return {"stock_data": stock_data}
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)