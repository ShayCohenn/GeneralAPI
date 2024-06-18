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
    excel = "excel"


class Interval(Enum):
    ONE_MINUTE = "1m"
    TWO_MINUTES = "2m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    SIXTY_MINUTES = "60m"
    NINETY_MINUTES = "90m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    FIVE_DAYS = "5d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"

def verify_ticker(ticker: str) -> yf.Ticker:
    """Verify if the ticker is valid by checking if it has historical data."""
    data = yf.Ticker(ticker)
    if not data.history(period="1d").empty:
        return data
    raise HTTPException(status_code=400, detail={"error": f"Could not find stock symbol {ticker}"})


def str_to_date(date: Union[str, None]) -> datetime:
    try:
        if date is None:
            date_formatted = datetime.strptime(datetime.now().strftime("%d-%m-%Y"),"%d-%m-%Y")
        else:
            date_formatted = datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        raise HTTPException(status_code=400, detail={"error": "Invalid date format"})
    return date_formatted

def validate_dates(start: str, end: str) -> None:
    """Validate the start and end dates and the interval."""
    start_date = str_to_date(start)
    end_date = str_to_date(end)
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail={"error": "Start date cannot be the same or after end date"})
    if start_date > datetime.now() or end_date > datetime.now():
        raise HTTPException(status_code=400, detail={"error": "Cannot get stock data from the future"})

def validate_column(columns: Union[str, None]) -> list[str]:
    valid_columns = ['Date', 'High', 'Low', 'Open', 'Close', 'Adj Close', 'Volume']
    if columns is None:
        return valid_columns
    selected_columns = []
    columns_list = columns.split(',')

    for col in columns_list:
        col_capitalized = col.strip().title()
        if col_capitalized in valid_columns:
            selected_columns.append(col_capitalized)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid column '{col}' requested.")

    selected_columns.insert(0,'Date')
    return selected_columns

def main_stock_data(ticker: str, start: str, end: str, interval: Interval) -> pd.DataFrame:
    validate_dates(start, end)
    
    start_date = str_to_date(start)
    end_date = str_to_date(end)
    
    data: pd.DataFrame = yf.download(ticker, start=start_date, end=end_date, interval=interval.value)
    if data.empty:
        raise HTTPException(status_code=404, detail={"error": "No data found for the given period"})
    
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    return data

# ---------------------------------------------------------------- Endpoints ----------------------------------------------------------------

@router.get("/general-info", response_class=ORJSONResponse)
@rate_limiter(max_requests_per_second=1, max_requests_per_day=200)
async def get_general_info(request: Request, ticker: str) -> ORJSONResponse:
    """Returns general information about a company."""
    data = verify_ticker(ticker)
    info = data.info
    return ORJSONResponse(content=info, status_code=200)

@router.get("/current-value", response_class=ORJSONResponse)
@rate_limiter(max_requests_per_second=1, max_requests_per_day=200)
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
            "date": datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        }
    }
    return ORJSONResponse(content=information, status_code=200)

@router.get("/currency-convert", response_class=ORJSONResponse)
@rate_limiter(max_requests_per_second=1, max_requests_per_day=200)
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
            "date": datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        }
    }
    return ORJSONResponse(content=information, status_code=200)

@router.get("/stock-data.{format}")
@rate_limiter(max_requests_per_second=1, max_requests_per_day=100)
async def get_stock_data(
    request: Request,
    format: Format = Path(..., description="The format in which to retrieve the stock data"),
    ticker: str = Query(..., description="The stock ticker symbol"),
    start: str = Query(..., description="The start date in dd-mm-yyyy format"),
    end: str = Query(None, description="The end date in dd-mm-yyyy format. Defaults to today if not provided"),
    interval: Interval = Query(Interval.ONE_DAY, description="The interval for the stock data"),
    columns: str = Query(None, description="Comma-separated list of columns to export, at least 1 column is required")):
    """Fetch stock data for a given ticker and date range."""
    verified_ticker: yf.Ticker = verify_ticker(ticker)
    data: pd.DataFrame = main_stock_data(ticker, start, end, interval)

    selected_columns: list[str] = validate_column(columns)
    data = data[selected_columns]

    format = format.value
    
    if format == "json":
        stock_data = data.to_dict(orient='records')
        information = {
            "info": {
                "ticker": ticker,
                "company": verified_ticker.info.get("longName", "N/A"),
                "currency": verified_ticker.info.get("currency", "N/A"),
                "interval": interval,
                "start_date": start,
                "end_date": end or datetime.now().strftime("%d-%m-%Y")
            },
            "stock_data": stock_data
        }
        return ORJSONResponse(content=information, status_code=200)
    
    elif format == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            data.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        filename = f'{ticker}_{start}-{end or datetime.now().strftime("%d-%m-%Y")}-{interval}.xlsx'
        return StreamingResponse(
            output,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    
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