from fastapi import APIRouter, HTTPException, Depends
from vonage import Client, Sms
from constants import SMS_KEY, SECRET
from pydantic import BaseModel
from ..auth.dependency import get_api_key

router = APIRouter()

class SmsRequest(BaseModel):
    from_user: str
    to: str
    text: str

def send_sms(phone_num: str, msg: str, from_user: str) -> None:
    client: Client = Client(key=SMS_KEY, secret=SECRET)
    sms: Sms = Sms(client)

    responseData = sms.send_message(
        {
            "from": from_user,
            "to": phone_num,
            "text": msg,
            'type':'unicode'
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

@router.post("/send")
async def send_sms_endpoint(sms_request: SmsRequest, user=Depends(get_api_key)):
    try:
        send_sms(sms_request.to, sms_request.text, sms_request.from_user)
        return {"message": "SMS sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send SMS: {str(e)}")
