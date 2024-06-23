from datetime import datetime
import pandas as pd
import yfinance as yf
from fastapi import APIRouter, Request, HTTPException, Query, Path
from fastapi.responses import ORJSONResponse
from core.rate_limiter import rate_limiter
from .functions import (verify_ticker, validate_column, main_stock_data, calculate_period_change,
                        stock_data_format_json, stock_data_format_excel, stock_data_format_csv, stock_data_format_html,
                        Format, Interval, ValidColumns)

router = APIRouter()

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
    information: dict = {
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

    data: pd.DataFrame = main_stock_data(verified_ticker, start, end, interval)

    selected_columns: list[str] = validate_column(columns)

    if ValidColumns.CHANGE.value in columns.lower():
        data = calculate_period_change(data)

    data = data[selected_columns].round(2)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Date'] = data['Date'].dt.strftime('%d-%m-%Y')

    format = format.value
    
    if format == Format.json.value:
        return stock_data_format_json(data=data, ticker=verified_ticker, interval=interval.value, start=start, end=end)
    elif format == Format.excel.value:
        return stock_data_format_excel(data=data, ticker=ticker, interval=interval.value, start=start, end=end)
    elif format == Format.csv.value:
        return stock_data_format_csv(data=data, ticker=ticker, interval=interval.value, start=start, end=end)
    elif format == Format.html.value:
        return stock_data_format_html(data=data)