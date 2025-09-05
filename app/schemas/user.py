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
    username: Optional[str] = None       # ✅ default
    wallet_address: Optional[str] = None # ✅ default
    auth_provider: Optional[str] = None  # ✅ default
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }