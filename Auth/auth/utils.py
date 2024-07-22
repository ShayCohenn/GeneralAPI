import jwt
import asyncio
import secrets
import hashlib
from enum import Enum
from typing import Optional, Union
from datetime import datetime, timedelta, timezone
from fastapi import status, HTTPException, Cookie, Depends, Response
from jwt.exceptions import InvalidTokenError
from .models import TokenData, User
from core.db import users_db, redis_client
from core.config import Secrets

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

class UserSearchField(Enum):
    USERNAME = "username"
    EMAIL = "email"
    API_KEY = "api_key"
    VERIFICATION_TOKEN = "verification_token"
    RESET_TOKEN = "reset_token"


def get_password_hash(password: str) -> str:
    salt = hashlib.sha256(Secrets.SECRET_KEY.encode('utf-8')).digest()
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 1000)
    return key.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    stored_password_hash = get_password_hash(plain_password)
    return secrets.compare_digest(stored_password_hash, hashed_password)

def create_api_key() -> str:
    """Generate a unique API key"""
    while True:
        api_key = secrets.token_hex(64)
        if not users_db.find_one({"api_key": api_key}):
            return api_key

def generate_verification_token() -> str:
    """Generate a unique verification token"""
    while True:
        verification_token = secrets.token_urlsafe(64)
        if not users_db.find_one({"verification_token": verification_token}):
            return verification_token

async def remove_expired() -> None:
    """Remove expired unverified users and expired reset password tokens"""
    expiration_time = timedelta(minutes=15)
    while True:
        current_time = datetime.now(timezone.utc)
        # Remove expired reset password tokens
        expired_tokens = users_db.find({"reset_token_created_at": {"$lt": current_time - expiration_time}})
        for token in expired_tokens:
            users_db.update_one({"_id": token["_id"]}, {"$unset": {"reset_token": "", "reset_token_created_at": ""}})
        # Remove unverified users
        expired_unverified_users = users_db.find({"created_at": {"$lt": current_time - expiration_time, "verified": False}})
        for user in expired_unverified_users:
            users_db.delete_one({"_id": user["_id"], "verified": False})
        await asyncio.sleep(60)


def get_user(search_field: UserSearchField, query: str) -> Optional[User]:
    user_record: User = users_db.find_one({search_field.value: query})
    return user_record


def authenticate_user(username: str, password: str) -> User:
    user_record: User = users_db.find_one({"username": username})
    if not user_record or not user_record['password'] or not verify_password(password, user_record['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_record


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode: dict = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, Secrets.SECRET_KEY, algorithm=Secrets.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return create_access_token(data, expires_delta)


async def get_current_user(access_token: Optional[str] = Cookie(None)) -> User:
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if access_token is None:
            raise credentials_exception
        
        payload: dict = jwt.decode(access_token, Secrets.SECRET_KEY, algorithms=[Secrets.ALGORITHM])
        username: str = payload["username"]
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user: Optional[User] = get_user(UserSearchField.USERNAME, token_data.username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user['verified'] or not current_user['active']:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def set_cookies(username: str, response: Response) -> dict[str, str]:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    access_token = create_access_token(
        data={"username": username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"username": username}, expires_delta=refresh_token_expires
    )
    
    # Store refresh token in Redis with expiration time
    redis_client.setex(f"refresh_token:{username}", int(refresh_token_expires.total_seconds()), refresh_token)
    
    # Set cookies in the response
    response.set_cookie(
        key="access_token", value=access_token, httponly=True, max_age=access_token_expires.total_seconds(), path="/"
    )
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, max_age=refresh_token_expires.total_seconds(), path="/"
    )
    return {"access_token": access_token, "refresh_token": refresh_token}

async def startup_event() -> None:
    asyncio.create_task(remove_expired())