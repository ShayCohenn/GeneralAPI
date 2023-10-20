from fastapi import FastAPI
from QR.qr import router as qr_router
from finance.stocks import router as stocks_router

app = FastAPI()

app.include_router(qr_router, prefix="/qr")
app.include_router(stocks_router, prefix="/finance")