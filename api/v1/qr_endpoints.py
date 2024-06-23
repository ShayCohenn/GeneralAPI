import segno
import base64
import tempfile
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import ORJSONResponse
from core.rate_limiter import rate_limiter

router = APIRouter()

class QrParams(BaseModel):
    data: str
    back_color: str = "white"
    front_color: str = "black"
    scale: int = 20
    border_size: int = 1
    border_color: str = "white"

@router.post("/generate")
@rate_limiter(max_requests_per_second=1, max_requests_per_day=2)
async def generate_qr_code(request: Request, qr_params: QrParams) -> ORJSONResponse:
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            # Create a QR code and save it to the temporary file
            qr_code = segno.make_qr(qr_params.data)
            qr_code.save(temp_file.name, scale=qr_params.scale, border=qr_params.border_size, light=qr_params.back_color, dark=qr_params.front_color, quiet_zone=qr_params.border_color)

        # Read the content of the temporary file
        with open(temp_file.name, "rb") as file:
            img_base64 = base64.b64encode(file.read()).decode()

        return ORJSONResponse(status_code=200, content={"QR_URL": f"data:image/png;base64,{img_base64}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
