from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from QR.qr import router as qr_router
from finance.endpoints import router as stocks_router
from entertainment.endpoints import router as jokes_router

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You should specify the allowed origins instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qr_router, prefix="/qr")
app.include_router(stocks_router, prefix="/finance")
app.include_router(jokes_router, prefix="/entertainment")
