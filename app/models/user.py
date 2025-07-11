
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(index=True, unique=True)
    username: Optional[str] = Field(default=None, index=True)
    password_hash: Optional[str] = None  # null if OAuth or Web3 only
    wallet_address: Optional[str] = Field(default=None, index=True)
    auth_provider: Optional[str] = Field(default="credentials")  # credentials | oauth | web3
    created_at: datetime = Field(default_factory=datetime.utcnow)