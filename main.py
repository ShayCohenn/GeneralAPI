from fastapi import FastAPI
from QR.qr import router as qr_router

app = FastAPI()

app.include_router(qr_router, prefix="/qr")