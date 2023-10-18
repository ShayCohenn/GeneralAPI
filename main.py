from fastapi import FastAPI
import segno
from io import BytesIO
import base64
import tempfile  # Import the tempfile module
import uvicorn

app = FastAPI()

@app.get("/generate_qr")
def generate_qr_code(data: str, back_color: str = "white", front_color: str = "black"):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        # Create a QR code and save it to the temporary file
        qr = segno.make_qr(data)
        qr.save(temp_file.name, scale=20, border=1, light=back_color, dark=front_color,)

    # Read the content of the temporary file
    with open(temp_file.name, "rb") as file:
        img_base64 = base64.b64encode(file.read()).decode()

    return {"QR_URL": f"data:image/png;base64,{img_base64}"}

if __name__ == "__main":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
