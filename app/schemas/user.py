from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    wallet_address: Optional[str] = None
    username: Optional[str] = None

class UserRead(BaseModel):
    id: str
    email: EmailStr
    username: Optional[str]
    wallet_address: Optional[str]
    auth_provider: str
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    wallet_address: Optional[str] = None