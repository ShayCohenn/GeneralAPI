from fastapi import APIRouter, HTTPException, Request
from sports.methods import scrape_soccer_matches
from slowapi.util import get_remote_address
from rate_limit import limiter

router = APIRouter()

@router.get("/football/today")
@limiter.limit("1 per 2 seconds", key_func=get_remote_address)
def get_todays_football(request: Request):
    return scrape_soccer_matches(day=0)

@router.get("/football/tomorrow")
@limiter.limit("1 per 2 seconds", key_func=get_remote_address)
def get_todays_football(request: Request):
    return scrape_soccer_matches(day=1)

@router.get("/football/2days")
@limiter.limit("1 per 2 seconds", key_func=get_remote_address)
def get_todays_football(request: Request):
    return scrape_soccer_matches(day=2)