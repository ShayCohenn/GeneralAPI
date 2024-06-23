import smtplib
from datetime import datetime
from typing import Optional
import re
from fastapi import HTTPException, Header
from cachetools import LRUCache, TTLCache
from core.config import EmailConfig
from core.db import users_db

cache = LRUCache(maxsize=2048)
timed_cache = TTLCache(ttl=120, maxsize=2048)


def validate_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def validate_input(input_str: str) -> bool:
    return bool(re.match(r'^[a-zA-Z0-9\s]*$', input_str))


async def get_api_key(x_api_key: str = Header(...)):
    user = users_db.find_one({"api_key": x_api_key})
    if user is None:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return user


def create_email_message(from_user: str, msg: str, subject: str) -> str:
    """Construct the email"""
    message = f"Subject: {subject}\n"
    message += f"From: {from_user} <{EmailConfig.FROM_EMAIL}>\n\n"
    message += msg
    message = message.encode('utf-8')
    return message

def send_email(message: str, to_user: str) -> None:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(EmailConfig.FROM_EMAIL, EmailConfig.PASSWORD)
        connection.sendmail(from_addr=EmailConfig.FROM_EMAIL, to_addrs=to_user, msg=message)

def get_current_date() -> str:
    return datetime.now().strftime("%d-%m-%Y")


def str_to_date(date: Optional[str]) -> datetime:
    try:
        if date is None:
            date_formatted = datetime.strptime(get_current_date(),'%d-%m-%Y')
        else:
            date_formatted = datetime.strptime(date, '%d-%m-%Y')
    except ValueError:
        raise HTTPException(status_code=400, detail={"error": "Invalid date format"})
    return date_formatted