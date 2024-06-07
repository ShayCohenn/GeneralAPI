from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from .scraping import scrape_soccer_matches
from constants import MAIN_ERROR_MESSAGE

router = APIRouter()

@router.get("/football/matches")
def get_football_matches(day: int = 0) -> ORJSONResponse:
    try:
        response = scrape_soccer_matches(day=day)
        if len(response) > 0:
            return response
        return ORJSONResponse(status_code=200, content={"error":"could not find anything for this day"})
    except:
        return ORJSONResponse(status_code=500, content=MAIN_ERROR_MESSAGE)