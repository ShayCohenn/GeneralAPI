import re
import smtplib
from core.config import EmailConfig

def validate_email(email: str) -> bool:
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

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