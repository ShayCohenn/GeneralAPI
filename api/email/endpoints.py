from pydantic import BaseModel, Field, EmailStr
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import ORJSONResponse
from ..auth.dependency import get_api_key
from constants import FROM_EMAIL, PASSWORD, validate_email
from .functionality import create_message, send_email

router = APIRouter()

class EmailRequest(BaseModel):
    message: str
    to_users: list[EmailStr] = Field(..., max_length=10)
    from_user: str = "noreply"
    subject: str

@router.post('/send')
async def send_email_endpoint(email_request: EmailRequest, user=Depends(get_api_key)) -> ORJSONResponse:
    """Sends an email using smtplib"""
    try:
        if len(email_request.to_users) > 10:
            raise HTTPException(status_code=400, detail="Cannot send more than 10 emails at a time")
        for user in email_request.to_users:
            if validate_email(user):
                message = create_message(from_user=email_request.from_user, subject=email_request.subject, msg=email_request.message)
                send_email(message, user)
        return ORJSONResponse(content={"message": "Email sent successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send Email: {str(e)}")
