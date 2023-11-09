from fastapi import APIRouter, HTTPException, Request
from weather.methods import get_general_weather, get_current_temp
from rate_limit import limiter
from sports.methods import scrape_soccer_matches

router = APIRouter()

@router.get("/football/today")
def get_todays_football():
    return scrape_soccer_matches(day=0)

@router.get("/football/tomorrow")
def get_todays_football():
    return scrape_soccer_matches(day=1)

@router.get("/football/2days")
def get_todays_football():
    return scrape_soccer_matches(day=2)