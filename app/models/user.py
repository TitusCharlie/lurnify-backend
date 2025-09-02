from __future__ import annotations
from sqlmodel import SQLModel, Field
from sqlalchemy.orm import Mapped, relationship
from typing import Optional, List
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    email: Optional[str] = Field(default=None, unique=True, index=True)
    hashed_password: Optional[str] = Field(default=None)
    wallet_address: Optional[str] = Field(default=None, unique=True, index=True)
    social_provider: Optional[str] = Field(default=None)   # e.g., "google", "twitter"
    social_id: Optional[str] = Field(default=None)         # provider user ID
    nonce: Optional[str] = Field(default=None)             # for wallet challenge
    profile_picture: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # ✅ relationships
    communities: Mapped[List["Community"]] = relationship(back_populates="creator")
    memberships: Mapped[List["Membership"]] = relationship(back_populates="user")
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
