import smtplib
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from ..auth.dependency import get_api_key
from constants import FROM_EMAIL, PASSWORD, validate_email

router = APIRouter()

class EmailRequest(BaseModel):
    message: str
    to_user: str
    from_user: str = "noreply"
    subject: str

def create_message(from_user: str, msg: str, subject: str) -> str:
    """Construct the email"""
    message = f"Subject: {subject}\n"
    message += f"From: {from_user} <{FROM_EMAIL}>\n\n"
    message += msg
    message = message.encode('utf-8')
    return message

def send_email(message: str, to_user: str) -> None:
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(FROM_EMAIL, PASSWORD)
            connection.sendmail(from_addr=FROM_EMAIL, to_addrs=to_user, msg=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send Email: {str(e)}")

@router.post('/send')
async def send_email_endpoint(email_request: EmailRequest, user=Depends(get_api_key)):
    """Sends an email using smtplib"""
    if not validate_email(email_request.to_user):
        raise HTTPException(status_code=400, detail="Invalid email format")
    try:
        message = create_message(from_user=email_request.from_user, subject=email_request.subject, msg=email_request.message)
        send_email(message, email_request.to_user)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send Email: {str(e)}")
