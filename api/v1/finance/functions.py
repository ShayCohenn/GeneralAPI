import io
from enum import Enum
from typing import Union
from datetime import datetime
import pandas as pd
import yfinance as yf
from fastapi import HTTPException
from fastapi.responses import ORJSONResponse, StreamingResponse, HTMLResponse
from core.utils import str_to_date, get_current_date

# ---------------------------------------------------------------- Enums ----------------------------------------------------------------

class Format(Enum):
    json = "json"
    csv = "csv"
    html = "html"
    excel = "excel"

class ValidColumns(Enum):
    DATE = 'date'
    HIGH = 'high'
    LOW = 'low'
    OPEN = 'open'
    CLOSE = 'close'
    DIVIDENDS = 'dividends'
    VOLUME = 'volume'
    STOCK_SPLITS = 'stock splits'
    CHANGE = 'change'

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

# ---------------------------------------------------------------- Functions ----------------------------------------------------------------

def verify_ticker(ticker: str) -> yf.Ticker:
    data = yf.Ticker(ticker)
    if not data.history(period="1d").empty:
        return data
    raise HTTPException(status_code=400, detail={"error": f"Could not find stock symbol {ticker}"})

# -------------------------- /stock-data enpoint functions --------------------------------

def validate_dates(start: str, end: str) -> None:
    """Validate the start and end dates and the interval."""
    start_date = str_to_date(start)
    end_date = str_to_date(end)
    if start_date >= end_date:
        raise HTTPException(status_code=400, detail={"error": "Start date cannot be the same or after end date"})
    if start_date > datetime.now() or end_date > datetime.now():
        raise HTTPException(status_code=400, detail={"error": "Cannot get stock data from the future"})


def validate_column(columns: Union[str, None]) -> list[str]:
    valid_columns = [col.value.title() for col in ValidColumns]
    if columns is None:
        return valid_columns
    
    columns_list = columns.split(',')
    selected_columns = []
    
    for col in columns_list:
        col_name = col.title()
        if col_name in valid_columns:
            if col_name == 'Change':
                selected_columns.extend(['Interval Change (%)', 'Total Change (%)'])
            else:
                selected_columns.append(col_name)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid column '{col}' requested.")
    
    selected_columns.insert(0, 'Date')
    return selected_columns


def main_stock_data(ticker: yf.Ticker, start: str, end: str, interval: Interval) -> pd.DataFrame:
    validate_dates(start, end)
    
    start_date = str_to_date(start)
    end_date = str_to_date(end)
    
    data: pd.DataFrame = ticker.history(start=start_date, end=end_date, interval=interval.value)
    if data.empty:
        raise HTTPException(status_code=404, detail={"error": "No data found for the given period"})
    
    data = data.reset_index()
    data['Date'] = pd.to_datetime(data['Date']).dt.date
    return data


def calculate_period_change(data: pd.DataFrame) -> pd.DataFrame:
    previous_close = data.iloc[0]['Close']
    initial_close = previous_close
    data['Interval Change (%)'] = 0.0
    data['Total Change (%)'] = 0.0
    
    for i in range(1, len(data)):
        current_close = data.iloc[i]['Close']

        period_growth = ((current_close - previous_close) / previous_close) * 100
        data.at[data.index[i], 'Interval Change (%)'] = period_growth

        total_growth = ((current_close - initial_close) / initial_close) * 100
        data.at[data.index[i], 'Total Change (%)'] = total_growth

        previous_close = current_close
    
    return data

# --------------------------------------- Stock Data Formats ---------------------------------------
def stock_data_format_json(data: pd.DataFrame, ticker: yf.Ticker, interval: str, start: str, end: Union[str, None]) -> ORJSONResponse:
    stock_data = data.to_dict(orient='records')
    information = {
        "info": {
            "ticker": ticker.info.get("symbol", "N/A"),
            "company": ticker.info.get("longName", "N/A"),
            "currency": ticker.info.get("currency", "N/A"),
            "interval": interval,
            "start_date": start,
            "end_date": end or get_current_date(),
        },
        "stock_data": stock_data
    }
    return ORJSONResponse(content=information, status_code=200)

def stock_data_format_excel(data: pd.DataFrame, ticker: str, interval: str, start: str, end: Union[str, None]) -> StreamingResponse:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    filename = f'{ticker}_{start}-{end or get_current_date()}-{interval}.xlsx'
    return StreamingResponse(
        output,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

def stock_data_format_csv(data: pd.DataFrame, ticker: str, interval: str, start: str, end: Union[str, None]) -> StreamingResponse:
    csv_buffer = io.StringIO()
    data.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    filename = f'{ticker}_{start}-{end or get_current_date()}-{interval}.csv'
    return StreamingResponse(
        csv_buffer,
        media_type='text/csv',
        headers={'Content-Disposition': f'attachment;filename={filename}'}
    )

def stock_data_format_html(data: pd.DataFrame) -> HTMLResponse:
    html_content = data.to_html(index=False)
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ border: 1px solid #dddddd; padding: 10px; text-align: center; }}
            th {{ background-color: #f2f2f2; }}
            .table-striped tbody tr:nth-of-type(odd) {{ background-color: #f5f5f5; }}
            .table-bordered th, .table-bordered td {{ border: 1px solid #dddddd; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)