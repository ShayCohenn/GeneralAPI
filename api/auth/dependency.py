from fastapi import HTTPException, Header
from constants import users_db

async def get_api_key(x_api_key: str = Header(...)):
    user = users_db.find_one({"api_key": x_api_key})
    if user is None:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return user
