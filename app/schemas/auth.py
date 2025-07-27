# from app.services.auth import create_user_with_wallet
from sqlmodel import Session
from fastapi import APIRouter, Depends
from app.core.database import get_session
from pydantic import BaseModel, EmailStr
from typing import Optional

class SignupRequest(BaseModel):
    email: str
    username: str
    password: str
    wallet_address: str | None = None

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserLogin(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    wallet_address: Optional[str] = None
