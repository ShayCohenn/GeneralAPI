from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.endpoints import router

# ----------------------------------------------- App Initialization ----------------------------------------------------------------------

app = FastAPI()

# ----------------------------------------------- Enable CORS for all origins -------------------------------------------------------------


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.exception_handler(404)
# async def custom_404_handler(_, __):
#     return ORJSONResponse(status_code=404, content=Messages.MAIN_404_MESSAGE)

# @app.exception_handler(500)
# async def custom_500_handler(_, __):
#     return ORJSONResponse(status_code=500, content=Messages.MAIN_ERROR_MESSAGE)

# ----------------------------------------------- Including The Routers -------------------------------------------------------------------

app.include_router(router, prefix='')