import os
import pandas as pd
import yfinance as yf
from datetime import datetime
from typing import Any, Union
from fastapi import APIRouter, HTTPException
from fastapi.responses import ORJSONResponse, FileResponse
from starlette.background import BackgroundTask

router = APIRouter()

def verify_ticker(ticker: str) -> Union[yf.Ticker, HTTPException]:
    """Verify if the ticker is valid by checking if it has historical data."""
    data = yf.Ticker(ticker)
    if not data.history(period="1d").empty:
        return data
    raise HTTPException(status_code=400, detail={"error": f"Could not find stock symbol {ticker}"})


def validate_dates(start: str, end: str, interval: str) -> None:
    """Validate the start and end dates and the interval."""
    try:
        start_date = datetime.strptime(start, '%d-%m-%Y')
    except ValueError:
        raise HTTPException(status_code=400, detail={"error": "Invalid start date format"})

    try:
        end_date = datetime.now() if end.lower() in ["today", "now"] else datetime.strptime(end, '%d-%m-%Y')
    except ValueError:
        raise HTTPException(status_code=400, detail={"error": "Invalid end date format"})
    
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail={"error": "Start date cannot be the same or after end date"})
    if start_date > datetime.now() or end_date > datetime.now():
        raise HTTPException(status_code=400, detail={"error": "Cannot get stock data from the future"})
    
    valid_intervals = {"1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"}
    if interval not in valid_intervals:
        raise HTTPException(status_code=400, detail={"error": f"Invalid interval, please choose one of the following: {', '.join(valid_intervals)}"})
    
def main_stock_data(ticker: str, start: str, end: str, interval: str) -> pd.DataFrame:
    validate_dates(start, end, interval)
    
    start_date = datetime.strptime(start, '%d-%m-%Y')
    end_date = datetime.now() if end.lower() in ["today", "now"] else datetime.strptime(end, '%d-%m-%Y')
    
    data: pd.DataFrame = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    if data.empty:
        raise HTTPException(status_code=404, detail={"error": "No data found for the given period"})
    
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    return data

# ---------------------------------------------------------------- Endpoints ----------------------------------------------------------------

@router.get("/general-info", response_class=ORJSONResponse)
def get_general_info(ticker: str) -> ORJSONResponse:
    """Returns general information about a company."""
    data = verify_ticker(ticker)
    info = data.info
    return ORJSONResponse(content=info, status_code=200)

@router.get("/current-value", response_class=ORJSONResponse)
def get_value(ticker: str) -> ORJSONResponse:
    """Returns current value of a company's stock."""
    data = verify_ticker(ticker)
    current_price = data.history(period="1d")['Close'].iloc[-1]
    information: dict[str, Any] = {
        "current_value": current_price,
        "info": {
            "ticker": ticker,
            "company": data.info.get("longName", "N/A"),
            "currency": data.info.get("currency", "N/A"),
            "date": datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        }
    }
    return ORJSONResponse(content=information, status_code=200)

@router.get("/currency-convert", response_class=ORJSONResponse)
def get_exchange_rate(from_curr: str, to_curr: str, amount: float = 1):
    """Currency converter, provide from currency (from_curr) to currency (to_curr) and an amount to convert (default is 1)."""
    data = yf.Ticker(f'{from_curr}{to_curr}=X')
    if not data.history(period="1d").empty:
        result = data.history(period="1d")["Close"].iloc[-1] * amount
        information = {
            "result": result,
            "info": {
                "from_curr": from_curr.upper(),
                "to_curr": to_curr.upper(),
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
        }
        return ORJSONResponse(content=information, status_code=200)
    raise HTTPException(status_code=404, detail={"error": f"Could not find exchange rate for {from_curr}/{to_curr}"})

@router.get("/stock-data", response_class=ORJSONResponse)
async def get_stock_data(ticker: str, start: str, end: str, interval: str = "1d"):
    """Fetch stock data for a given ticker and date range."""
    verified_ticker = verify_ticker(ticker)
    data: pd.DataFrame = main_stock_data(ticker, start, end, interval)
    stock_data = data.to_dict(orient='records')
    information = {
        "info": {
            "ticker": ticker,
            "company": verified_ticker.info.get("longName", "N/A"),
            "currency": verified_ticker.info.get("currency", "N/A"),
            "interval": interval,
            "start_date": start,
            "end_date": end
        },
        "stock_data": stock_data
    }
    return ORJSONResponse(content=information, status_code=200)

def cleanup(file_path: str):
    os.remove(file_path)

@router.get("/stock-data-download.csv", response_class=FileResponse)
async def stock_data_download(ticker: str, start: str, end: str, interval: str = "1d"):
    verify_ticker(ticker)
    data: pd.DataFrame = main_stock_data(ticker, start, end, interval)
    csv_filename = f'{ticker}_{start}-{end}-{interval}.csv'
    data.to_csv(csv_filename, index=False)
    
    task = BackgroundTask(cleanup, file_path=csv_filename)
    return FileResponse(csv_filename, filename=csv_filename, media_type='text/csv', background=task)