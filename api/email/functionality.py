import smtplib
from constants import FROM_EMAIL, PASSWORD

def create_message(from_user: str, msg: str, subject: str) -> str:
    """Construct the email"""
    message = f"Subject: {subject}\n"
    message += f"From: {from_user} <{FROM_EMAIL}>\n\n"
    message += msg
    message = message.encode('utf-8')
    return message

def send_email(message: str, to_user: str) -> None:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(FROM_EMAIL, PASSWORD)
        connection.sendmail(from_addr=FROM_EMAIL, to_addrs=to_user, msg=message)