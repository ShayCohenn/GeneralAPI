import asyncio
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from constants import users_db, validate_email, CURRENT_URL
from .functionality import get_password_hash, create_api_key, verify_password, generate_verification_token, startup_event
from ..email.functionality import send_email, create_message

router = APIRouter()

# Add the background task to remove expired tokens and unverified users from DB
router.add_event_handler("startup", startup_event)

# ---------------------------------------------------------------- Input models ----------------------------------------------------------------

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ResetPassword(BaseModel):
    email: str

class ForgotPassword(BaseModel):
    email: str
    new_password: str

# ---------------------------------------------------------------- Endpoints ----------------------------------------------------------------

@router.post("/register", response_class=JSONResponse, response_model=dict)
async def register(user: UserCreate):
    """Create a user, create a verification token and send a verification email"""
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
        "verification_token": verification_token,
        "created_at": datetime.now()
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
    """Login to get API key"""
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

@router.put("/reset-api-key")
async def reset_api_key(user: UserLogin):
    user_record = users_db.find_one({"username": user.username})

    if not user_record or not verify_password(user.password, user_record["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    if not user_record["verified"]:
        raise HTTPException(status_code=401, detail="User not verified")
    
    new_api_key: str = create_api_key()

    users_db.update_one({"_id": user_record["_id"]}, {"$set": {"api_key":new_api_key}})

    return JSONResponse(status_code=200, content={"message": "API key reset successful", "api_key": new_api_key})

@router.post("/forgot-password")
async def forgot_password(req: ForgotPassword):
    """
    Forgot password function
    Gets the email and the new password from the user
    Sends an email to the user to confirm the password change.

    If the user didn't confirm the password change in 15 minutes the token date and new password hash will be deleted. 

    Confirmation logic in the /confirm-reset-password endpoint
    """
    user_record = users_db.find_one({"email": req.email})
    
    if not user_record:
        raise HTTPException(status_code=404, detail="Email not found")
    
    if not user_record["verified"]:
        raise HTTPException(status_code=401, detail="User not verified")
    
    # Generating the reset token for the confimation of the password reset, a new password hash, and a date for deleting the token and new password after 15 minutes
    reset_token = generate_verification_token()
    hashed_password = get_password_hash(req.new_password)
    reset_token_created_at = datetime.now()
    
    # Adding the reset token date and new password hash to the user record
    users_db.update_one({"_id": user_record["_id"]}, {"$set": {"reset_token": reset_token, "reset_token_created_at": reset_token_created_at, "new_password": hashed_password}})
    
    message = create_message(
        from_user='GeneralAPI',
        msg=f'Please reset your password by clicking on the following link: {CURRENT_URL}/auth/confirm-reset-password?token={reset_token}&user={str(user_record["_id"])}',
        subject='Reset your password')
    send_email(message=message, to_user=req.email)
    
    return JSONResponse(content={"message": "Password reset email sent"}, status_code=200)

@router.get("/confirm-reset-password")
async def reset_password(token: str, user: str):
    user_record = users_db.find_one({"reset_token": token})
    
    if not user_record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    if datetime.now() > user_record["reset_token_created_at"] + timedelta(minutes=15):
        raise HTTPException(status_code=400, detail="Token expired")
    
    if str(user_record["_id"]) != user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    users_db.update_one({"_id": user_record["_id"]}, {"$set": {"password": user_record["new_password"]}, "$unset": {"reset_token": "", "new_password":"", "reset_token_created_at":""}})
    
    return JSONResponse(content={"message": "Password reset successful"}, status_code=200)
