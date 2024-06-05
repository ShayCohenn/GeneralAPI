import asyncio
import secrets
import bcrypt
from datetime import datetime, timedelta
from constants import users_db

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_api_key() -> str:
    """Generate a unique API key"""
    while True:
        api_key = secrets.token_hex(32)
        if not users_db.find_one({"api_key": api_key}):
            return api_key

def generate_verification_token() -> str:
    """Generate a unique verification token"""
    while True:
        verification_token = secrets.token_urlsafe(32)
        if not users_db.find_one({"verification_token": verification_token}):
            return verification_token

async def remove_expired() -> None:
    """Remove expired unverified users and expired reset password tokens"""
    expiration_time = timedelta(minutes=15)
    while True:
        # Remove expired reset password tokens
        expired_tokens = users_db.find({"reset_token_created_at": {"$lt": datetime.now() - expiration_time}})
        for token in expired_tokens:
            users_db.update_one({"_id": token["_id"]}, {"$unset": {"reset_token": "", "reset_token_created_at": ""}})
        # Remove unverified users
        expired_unverified_users = users_db.find({"created_at": {"$lt": datetime.now() - expiration_time}}, {"verified":False})
        for user in expired_unverified_users:
            users_db.delete_one({"_id": user["_id"], "verified": False})
        await asyncio.sleep(60)

async def startup_event() -> None:
    asyncio.create_task(remove_expired())