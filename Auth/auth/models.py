from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    password: Optional[str]
    api_key: Optional[str]
    verified: bool
    verification_token: Optional[str]
    created_at: str
    reset_token: Optional[str]
    reset_token_created_at: Optional[str]
    new_password: Optional[str]
    active: bool

class TokenData(BaseModel):
    username: Optional[str] = None

class Register(BaseModel):
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Email(BaseModel):
    email: str

class ConfirmResetPassword(BaseModel):
    token: str
    user: str
    new_password: str

class UserSignin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
