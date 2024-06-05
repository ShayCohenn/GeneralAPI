from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tempfile
import segno
import base64

router = APIRouter()

class QrParams(BaseModel):
    data: str
    back_color: str = "white"
    front_color: str = "black"
    scale:int = 20
    border_size:int = 1
    border_color:str = "white"

@router.post("/generate")
def generate_qr_code(qr: QrParams):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            # Create a QR code and save it to the temporary file
            qr = segno.make_qr(qr.data)
            qr.save(temp_file.name, scale=qr.scale, border=qr.border_size, light=qr.back_color, dark=qr.front_color, quiet_zone=qr.border_color)

        # Read the content of the temporary file
        with open(temp_file.name, "rb") as file:
            img_base64 = base64.b64encode(file.read()).decode()

        return JSONResponse(status_code=200, content={"QR_URL": f"data:image/png;base64,{img_base64}"})
    except Exception as e:
        raise HTTPException(detail=e, status_code=500)