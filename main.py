from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from core.config import Docs, Messages
from api.v1 import v1_router

# ----------------------------------------------- App Initialization ----------------------------------------------------------------------

app = FastAPI(title="GeneralAPI",description=Docs.DESCRIPTION, version=Docs.VERSION)

# ----------------------------------------------- Enable CORS for all origins -------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(404)
async def custom_404_handler(_, __):
    return ORJSONResponse(status_code=404, content=Messages.MAIN_404_MESSAGE)

@app.exception_handler(500)
async def custom_500_handler(_, __):
    return ORJSONResponse(status_code=500, content=Messages.MAIN_ERROR_MESSAGE)

# ----------------------------------------------- Including The Routers -------------------------------------------------------------------

app.include_router(v1_router, prefix="/v1")