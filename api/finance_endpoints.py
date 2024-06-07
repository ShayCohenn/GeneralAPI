from typing import Any
from datetime import datetime
import pandas as pd
import yfinance as yf
from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse
from constants import MAIN_ERROR_MESSAGE

router = APIRouter()

def verify_ticker(ticker: str) -> yf.ticker.Ticker:
    data = yf.Ticker(ticker)
    if not data.history(period="1d").empty:
        return data
    return None

@router.get("/general-info")
def get_general_info(ticker: str) -> ORJSONResponse:
    """Returns general information about a company"""
    data = verify_ticker(ticker)
    if data:
        info = data.info
        return ORJSONResponse(content=info, status_code=200)
    raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)

@router.get("/current-value")
def get_value(ticker: str) -> ORJSONResponse:
    """Returns current value of a company's stock"""
    try:
        data = verify_ticker(ticker)
        if data:
            current_price = data.history(period="1d")['Close'].iloc[-1]
            information: dict[str, Any] = {
                    "current_value": current_price,
                    "info":{
                        "ticker":ticker,
                        "company":data.info["longName"],
                        "currency":data.info["currency"],
                        "date":datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
                    }
                    }
            return ORJSONResponse(content=information, status_code=200)
        raise HTTPException(status_code=202, detail={"error":f"could not find stock symbol {ticker}"})
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)
    
@router.get("/currency-convert")
def get_exchange_rate(from_curr: str, to_curr: str, amount: float = 1) -> ORJSONResponse:
    """Currency converter, provide from currency(from_curr) to currency(to_curr) and an amount to convert (default is 1)"""
    try:
        data = verify_ticker(f'{from_curr}{to_curr}=X')
        if data:
            result = data.history(period="1d")["Close"].iloc[-1] * amount
            information = {
                    "result":result,
                    "info":{
                        "from_curr":from_curr.upper(),
                        "to_curr":to_curr.upper(),
                        "amount":amount,
                        "date":datetime.now().strftime("%Y-%m-%d")
                    }
                    }
            return ORJSONResponse(content=information, status_code=200)
        raise HTTPException(status_code=404, detail={"error":f"could not find exchange rate for {from_curr}/{to_curr}"})
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)
    
@router.get("/stock-data")
async def get_stock_data(ticker: str, start:str, end:str, interval:str = "1d") -> ORJSONResponse:
    try:
        try:
            start_date = datetime.strptime(start, '%d-%m-%Y')
        except:
            raise HTTPException(status_code=400, detail={"error":"invalid start date format"})
        try:
            end_date = datetime.now() if end.lower() in {"today","now"} else datetime.strptime(end, '%Y-%m-%d')
        except:
            raise HTTPException(status_code=400, detail={"error":"invalid end date format"})
        if start_date >= end_date:
            raise HTTPException(status_code=400, detail={"error":"start date cannot be the same or after end date"})
        if start_date > datetime.now() or end_date > datetime.now():
            raise HTTPException(status_code=400, detail={"error":"cannot get stock data from the future"})
        if interval not in {"1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"}:
            raise HTTPException(status_code=400, detail={"error":"invalid interval please choose one of the following: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo"})
        verified_ticker = verify_ticker(ticker)
        if not verified_ticker:
            raise HTTPException(status_code=400, detail={"error":f"could not find stock symbol {ticker}"})
        data: pd.DataFrame = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        data = data.reset_index()
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date'] = data['Date'].dt.date
        stock_data = data.to_dict(orient='records')
        information = {
            "info":{
                "ticker":ticker,
                "company":verified_ticker.info["longName"],
                "currency":verified_ticker.info["currency"],
                "interval":interval,
                "start_date":start_date.strftime("%Y-%m-%d"),
                "end_date":end_date.strftime("%Y-%m-%d")
            },
            "stock_data": stock_data
            }
        return ORJSONResponse(content=information, status_code=200)
    except:
        raise HTTPException(status_code=500, detail=MAIN_ERROR_MESSAGE)