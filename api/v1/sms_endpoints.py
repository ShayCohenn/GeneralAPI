from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field
from vonage import Client, Sms
from core.config import SMSConfig
from core.utils import get_api_key
from core.rate_limiter import rate_limiter

router = APIRouter()

class SmsRequest(BaseModel):
    from_user: str
    to: list[str] = Field(..., max_length=5)
    text: str

def send_sms(phone_num: str, msg: str, from_user: str) -> None:
    client: Client = Client(key=SMSConfig.SMS_KEY, secret=SMSConfig.SMS_SECRET)
    sms: Sms = Sms(client)

    response_data = sms.send_message(
        {
            "from": from_user,
            "to": phone_num,
            "text": msg,
            'type':'unicode'
        }
    )

    if response_data["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {response_data['messages'][0]['error-text']}")

@router.post("/send")
@rate_limiter(max_requests_per_second=1, max_requests_per_day=10)
async def send_sms_endpoint(sms_request: SmsRequest, user=Depends(get_api_key)):
    try:
        for phone_num in sms_request.to:
            send_sms(phone_num, sms_request.text, sms_request.from_user)
        return ORJSONResponse(content={"message": "SMS sent successfully"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send SMS: {str(e)}")
