from fastapi import APIRouter, HTTPException, Depends, Response, status
from fastapi.responses import ORJSONResponse
from datetime import datetime, timedelta
from constants import users_db, validate_email, CURRENT_URL, r
from ..email.functionality import send_email, create_message
from .models import Register, TokenResponse, UserSignin, ForgotPassword, User
from .functionality import (get_password_hash, create_api_key, get_user, generate_verification_token, 
                            startup_event, create_access_token, create_refresh_token, authenticate_user, get_current_active_user, 
                            ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS, UserSearchField)

router = APIRouter()

# Add the background task to remove expired tokens and unverified users from DB
router.add_event_handler("startup", startup_event)

# ---------------------------------------------------------------- Endpoints ----------------------------------------------------------------

@router.post("/register")
async def register(user: Register) -> ORJSONResponse:
    """Create a user, create a verification token and send a verification email"""
    if not validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if get_user(UserSearchField.USERNAME, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if get_user(UserSearchField.EMAIL, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

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

    return ORJSONResponse(content={"message":"User create successfuly, Please verify your email to get your API key"}, status_code=200)

@router.get("/get-api-key")
async def login(user_record: User = Depends(get_current_active_user)) -> ORJSONResponse:
    """Get API key""" 
    return ORJSONResponse(status_code=200, content={"api_key": user_record["api_key"]})

@router.post("/login", response_model=TokenResponse)
async def login_for_tokens(user: UserSignin, response: Response) -> TokenResponse:
    user_record = authenticate_user(user.username, user.password)
    if not user_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"username": user_record['username']}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"username": user_record['username']}, expires_delta=refresh_token_expires
    )
    
    # Store refresh token in Redis with expiration time
    r.setex(f"refresh_token:{user_record['username']}", int(refresh_token_expires.total_seconds()), refresh_token)
    
    # Set cookies in the response
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=access_token_expires.total_seconds())
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=refresh_token_expires.total_seconds())
    
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

@router.get("/verify-email")
async def verify_email(token: str) -> ORJSONResponse:
    user_record = get_user(UserSearchField.VERIFICATION_TOKEN, token)

    if not user_record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    api_key: str = create_api_key()

    users_db.update_one({"_id": user_record["_id"]}, {"$set": {"verified": True, "api_key":api_key}, "$unset": {"verification_token": ""}})
    
    return ORJSONResponse(status_code=200, content={"message":"User verified successfuly", "api-key":api_key})

@router.get("/reset-api-key")
async def reset_api_key(user: User = Depends(get_current_active_user)) -> ORJSONResponse:    
    new_api_key = create_api_key()
    users_db.update_one({"username": user['username']}, {"$set": {"api_key": new_api_key}})
    return ORJSONResponse(status_code=200, content={"message": "API key reset successful", "api_key": new_api_key})

@router.post("/forgot-password")
async def forgot_password(req: ForgotPassword) -> ORJSONResponse:
    """
    Forgot password function
    Gets the email and the new password from the user
    Sends an email to the user to confirm the password change.

    If the user didn't confirm the password change in 15 minutes the token date and new password hash will be deleted. 

    Confirmation logic in the /confirm-reset-password endpoint
    """
    user_record = get_user(UserSearchField.EMAIL, req.email)
    
    if not user_record:
        raise HTTPException(status_code=406, detail="Email not found")
    
    if not user_record["verified"]:
        raise HTTPException(status_code=406, detail="User not verified")
    
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
    
    return ORJSONResponse(content={"message": "Password reset email sent"}, status_code=200)

@router.get("/confirm-reset-password")
async def reset_password(token: str, user: str) -> ORJSONResponse:
    user_record = get_user(UserSearchField.RESET_TOKEN, token)
    
    if not user_record:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    if datetime.now() > user_record["reset_token_created_at"] + timedelta(minutes=15):
        raise HTTPException(status_code=400, detail="Token expired")
    
    if str(user_record["_id"]) != user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    users_db.update_one({"_id": user_record["_id"]}, {"$set": {"password": user_record["new_password"]}, "$unset": {"reset_token": "", "new_password":"", "reset_token_created_at":""}})
    
    return ORJSONResponse(content={"message": "Password reset successful"}, status_code=200)