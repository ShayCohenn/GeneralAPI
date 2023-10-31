from fastapi import APIRouter, HTTPException
import tempfile
import segno
import base64

router = APIRouter()

@router.get("/generate")
def generate_qr_code(data: str, back_color: str = "white", front_color: str = "black", scale:int = 20, border_size:int = 1, border_color:str = "white"):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            # Create a QR code and save it to the temporary file
            qr = segno.make_qr(data)
            qr.save(temp_file.name, scale=scale, border=border_size, light=back_color, dark=front_color, quiet_zone=border_color)

        # Read the content of the temporary file
        with open(temp_file.name, "rb") as file:
            img_base64 = base64.b64encode(file.read()).decode()

        return {"QR_URL": f"data:image/png;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
