from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


class Community(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    creator_id: str = Field(foreign_key="user.id")
    creator: "User" = Relationship(back_populates="communities")

    members: List["Membership"] = Relationship(back_populates="community")
    posts: List["Post"] = Relationship(back_populates="community")


class Membership(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    user_id: str = Field(foreign_key="user.id")
    community_id: str = Field(foreign_key="community.id")
    joined_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="memberships")
    community: "Community" = Relationship(back_populates="members")


class Post(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    community_id: str = Field(foreign_key="community.id")
    user_id: str = Field(foreign_key="user.id")

    community: "Community" = Relationship(back_populates="posts")
    user: "User" = Relationship(back_populates="posts")