from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from sqlalchemy.orm import Mapped
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Community(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    creator_id: str = Field(foreign_key="user.id")
    creator: Mapped[Optional["User"]] = Relationship(back_populates="communities")

    memberships: Mapped[List["Membership"]] = Relationship(back_populates="community")
    posts: Mapped[List["Post"]] = Relationship(back_populates="community")


class Membership(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    user_id: str = Field(foreign_key="user.id")
    community_id: str = Field(foreign_key="community.id")
    joined_at: datetime = Field(default_factory=datetime.now)

    user: Mapped[Optional["User"]] = Relationship(back_populates="memberships")
    community: Mapped[Optional[Community]] = Relationship(back_populates="memberships")


class Post(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    community_id: str = Field(foreign_key="community.id")
    user_id: str = Field(foreign_key="user.id")

    community: Mapped[Optional[Community]] = Relationship(back_populates="posts")
    user: Mapped[Optional["User"]] = Relationship(back_populates="posts")