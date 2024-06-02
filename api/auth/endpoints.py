import secrets
import hashlib
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from constants import users_db, validate_email

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_api_key() -> str:
    return secrets.token_hex(32)

@router.post("/register")
async def register(user: UserCreate):
    if users_db.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    if users_db.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    if not validate_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    hashed_password = get_password_hash(user.password)
    api_key = create_api_key()

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "api_key": api_key
    }
    users_db.insert_one(user_data)

    return {"message": "User created successfully", "api_key": api_key}

@router.post("/login")
async def login(user: UserLogin):
    user_record = users_db.find_one({"username": user.username})

    if not user_record or get_password_hash(user.password) != user_record["password"]:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful", "api_key": user_record["api_key"]}