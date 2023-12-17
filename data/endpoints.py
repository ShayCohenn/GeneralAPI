from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from constants import DEFAULT_LIMITER
from rate_limit import limiter

router = APIRouter()

@router.get("/test")
@limiter.limit(DEFAULT_LIMITER)
def test(request: Request):
    return {"msg":"test 3.0"}