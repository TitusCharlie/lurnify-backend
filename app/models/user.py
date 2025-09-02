from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    email: Optional[str] = Field(default=None, unique=True, index=True)
    hashed_password: Optional[str] = None
    wallet_address: Optional[str] = Field(default=None, unique=True, index=True)
    social_provider: Optional[str] = None   # e.g., "google", "twitter"
    social_id: Optional[str] = None         # provider user ID
    nonce: Optional[str] = None             # for wallet challenge
    profile_picture: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # ✅ relationships (SQLModel way)
    communities: List["Community"] = Relationship(back_populates="creator")
    memberships: List["Membership"] = Relationship(back_populates="user")
    posts: List["Post"] = Relationship(back_populates="user")
