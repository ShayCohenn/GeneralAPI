import io
from enum import Enum
import pandas as pd
import yfinance as yf
from datetime import datetime
from typing import Any, Union
from fastapi import APIRouter, Request, HTTPException, Query, Path
from fastapi.responses import ORJSONResponse, StreamingResponse, HTMLResponse
from rate_limiter import rate_limiter

router = APIRouter()

class Format(Enum):
    json = "json"
    csv = "csv"
    html = "html"

def verify_ticker(ticker: str) -> Union[yf.Ticker, HTTPException]:
    """Verify if the ticker is valid by checking if it has historical data."""
    data = yf.Ticker(ticker)
    if not data.history(period="1d").empty:
        return data
    raise HTTPException(status_code=400, detail={"error": f"Could not find stock symbol {ticker}"})


def str_to_date(date: str) -> datetime:
    try:
        date_formatted = datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        raise HTTPException(status_code=400, detail={"error": "Invalid date format"})
    return date_formatted

def validate_dates(start: str, end: str, interval: str) -> None:
    """Validate the start and end dates and the interval."""
    start_date = str_to_date(start)
    end_date = datetime.now() if end is None else str_to_date(end)
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
    end_date = datetime.now() if end is None else datetime.strptime(end, '%d-%m-%Y')
    
    data: pd.DataFrame = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    if data.empty:
        raise HTTPException(status_code=404, detail={"error": "No data found for the given period"})
    
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    return data

# ---------------------------------------------------------------- Endpoints ----------------------------------------------------------------

@router.get("/general-info", response_class=ORJSONResponse)
@rate_limiter(max_requests_per_second=1, max_requests_per_day=100)
async def get_general_info(request: Request, ticker: str) -> ORJSONResponse:
    """Returns general information about a company."""
    data = verify_ticker(ticker)
    info = data.info
    return ORJSONResponse(content=info, status_code=200)

@router.get("/current-value", response_class=ORJSONResponse)
@rate_limiter(max_requests_per_second=1, max_requests_per_day=100)
async def get_value(request: Request, ticker: str) -> ORJSONResponse:
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
@rate_limiter(max_requests_per_second=1, max_requests_per_day=100)
async def get_exchange_rate(request: Request, from_curr: str, to_curr: str, amount: float = 1):
    """Currency converter, provide from currency (from_curr) to currency (to_curr) and an amount to convert (default is 1)."""
    data = yf.Ticker(f'{from_curr.upper()}{to_curr.upper()}=X')
    if data.history(period="1d").empty:
        raise HTTPException(status_code=404, detail={"error": f"Could not find exchange rate for {from_curr}/{to_curr}"})
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

@router.get("/stock-data.{format}")
@rate_limiter(max_requests_per_second=1, max_requests_per_day=20)
async def get_stock_data(
    request: Request,
    format: str = Path(..., description="The format in which to retrieve the stock data"),
    ticker: str = Query(..., description="The stock ticker symbol"),
    start: str = Query(..., description="The start date in dd-mm-yyyy format"),
    end: str = Query(None, description="The end date in dd-mm-yyyy format. Defaults to today if not provided"),
    interval: str = Query("1d", description="The interval for the stock data")):
    """Fetch stock data for a given ticker and date range."""
    verified_ticker = verify_ticker(ticker)
    data: pd.DataFrame = main_stock_data(ticker, start, end, interval)
    
    if format == "json":
        stock_data = data.to_dict(orient='records')
        information = {
            "info": {
                "ticker": ticker,
                "company": verified_ticker.info.get("longName", "N/A"),
                "currency": verified_ticker.info.get("currency", "N/A"),
                "interval": interval,
                "start_date": start,
                "end_date": end or datetime.now().strftime('%d-%m-%Y')
            },
            "stock_data": stock_data
        }
        return ORJSONResponse(content=information, status_code=200)
    
    elif format == "csv":
        csv_buffer = io.StringIO()
        data.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        filename = f'{ticker}_{start}-{end or datetime.now().strftime("%d-%m-%Y")}-{interval}.csv'
        return StreamingResponse(
            csv_buffer,
            media_type='text/csv',
            headers={'Content-Disposition': f'attachment;filename={filename}'}
        )
    
    elif format == "html":
        html_content = data.to_html(index=False)
        return HTMLResponse(content=html_content, status_code=200)