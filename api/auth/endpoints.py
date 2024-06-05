from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from constants import users_db, validate_email, CURRENT_URL
from .functionality import get_password_hash, create_api_key, verify_password, generate_verification_token
from ..email.functionality import send_email, create_message

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(user: UserCreate):
    if users_db.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    if users_db.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    if not validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    hashed_password = get_password_hash(user.password)
    verification_token = generate_verification_token()

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "api_key": None,
        "verified": False,
        "verification_token": verification_token
    }
    users_db.insert_one(user_data)
    message = create_message(
        from_user='GeneralAPI', 
        msg=f"Please verify your email by clicking on the following link: {CURRENT_URL}/auth/verify-email?token={verification_token}",
        subject='Verify your email')
    send_email(message=message, to_user=user.email)

    return JSONResponse(content={"message":"User create successfuly, Please verify your email to get your API key"}, status_code=200)

@router.post("/login")
async def login(user: UserLogin):
    user_record = users_db.find_one({"username": user.username})

    if not user_record or not verify_password(user.password, user_record["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not user_record["verified"]:
        raise HTTPException(status_code=401, detail="User not verified")

    return JSONResponse(status_code=200, content={"message": "Login successful", "api_key": user_record["api_key"]})

@router.get("/verify-email")
async def verify_email(token: str):
    user_record = users_db.find_one({"verification_token": token})

    if not user_record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    api_key: str = create_api_key()

    users_db.update_one({"_id": user_record["_id"]}, {"$set": {"verified": True, "api_key":api_key}, "$unset": {"verification_token": ""}})
    
    return JSONResponse(status_code=200, content={"message":"User verified successfuly", "api-key":api_key})
