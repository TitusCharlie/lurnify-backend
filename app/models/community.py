from __future__ import annotations
from sqlmodel import SQLModel, Field
from sqlalchemy.orm import Mapped, relationship
from typing import Optional, List
from datetime import datetime
import uuid


class Community(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    creator_id: str = Field(foreign_key="user.id")
    creator: Mapped["User"] = relationship(back_populates="communities")

    members: Mapped[List["Membership"]] = relationship(back_populates="community")
    posts: Mapped[List["Post"]] = relationship(back_populates="community")


class Membership(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    user_id: str = Field(foreign_key="user.id")
    community_id: str = Field(foreign_key="community.id")
    joined_at: datetime = Field(default_factory=datetime.now)

    user: Mapped["User"] = relationship(back_populates="memberships")
    community: Mapped["Community"] = relationship(back_populates="members")


class Post(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    community_id: str = Field(foreign_key="community.id")
    user_id: str = Field(foreign_key="user.id")

    community: Mapped["Community"] = relationship(back_populates="posts")
    user: Mapped["User"] = relationship(back_populates="posts")
