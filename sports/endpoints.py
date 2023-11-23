from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sports.methods import scrape_soccer_matches
from rate_limit import limiter
from constants import MAIN_ERROR_MESSAGE, LARGE_LIMITER

router = APIRouter()

@router.get("/football/matches")
@limiter.limit(LARGE_LIMITER)
def get_football_matches(request: Request, day: int = 0):
    try:
        response = scrape_soccer_matches(day=day)
        if len(response) > 0:
            return response
        return JSONResponse(status_code=200, content={"error":"could not find anything for this day"})
    except:
        return JSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)