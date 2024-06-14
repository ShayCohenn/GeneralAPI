from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    password: str
    api_key: Optional[str]
    verified: bool
    verification_token: Optional[str]
    created_at: str
    reset_token: Optional[str]
    reset_token_created_at: Optional[str]
    new_password: Optional[str]

class TokenData(BaseModel):
    username: str

class Register(BaseModel):
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

class UserSignin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str