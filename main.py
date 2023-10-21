from fastapi import FastAPI
from QR.qr import router as qr_router
from finance.endpoints import router as stocks_router
from entertainment.endpoints import router as jokes_router

app = FastAPI()

app.include_router(qr_router, prefix="/qr")
app.include_router(stocks_router, prefix="/finance")
app.include_router(jokes_router, prefix="/entertainment")