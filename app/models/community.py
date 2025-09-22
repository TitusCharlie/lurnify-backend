# from __future__ import annotations
# from sqlmodel import SQLModel, Field
# from sqlalchemy.orm import Mapped, relationship
# from typing import Optional, List
# from datetime import datetime
# import uuid


# def generate_uuid() -> str:
#     return str(uuid.uuid4())


# class Community(SQLModel, table=True):
#     __tablename__ = "community"

#     id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
#     name: str
#     description: Optional[str] = None
#     created_at: datetime = Field(default_factory=datetime.now)

#     creator_id: str = Field(foreign_key="user.id")
#     creator: Mapped["User"] = relationship(back_populates="communities")

#     memberships: Mapped[List["Membership"]] = relationship(back_populates="community")
#     posts: Mapped[List["Post"]] = relationship(back_populates="community")


# class Membership(SQLModel, table=True):
#     __tablename__ = "membership"

#     id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
#     user_id: str = Field(foreign_key="user.id")
#     community_id: str = Field(foreign_key="community.id")
#     joined_at: datetime = Field(default_factory=datetime.now)

#     user: Mapped["User"] = relationship(back_populates="memberships")
#     community: Mapped["Community"] = relationship(back_populates="memberships")


# class Post(SQLModel, table=True):
#     __tablename__ = "post"

#     id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
#     content: str
#     created_at: datetime = Field(default_factory=datetime.now)

#     community_id: str = Field(foreign_key="community.id")
#     user_id: str = Field(foreign_key="user.id")

#     community: Mapped["Community"] = relationship(back_populates="posts")
#     user: Mapped["User"] = relationship(back_populates="posts")

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class Community(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    description: Optional[str] = None
    creator_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    members: List["Membership"] = Relationship(back_populates="community")
    posts: List["Post"] = Relationship(back_populates="community")
    courses: List["CommunityCourseLink"] = Relationship(back_populates="community")


class Membership(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    community_id: str = Field(foreign_key="community.id")
    role: str  # owner, admin, member
    joined_at: datetime = Field(default_factory=datetime.now)

    community: "Community" = Relationship(back_populates="members")


class Post(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    community_id: str = Field(foreign_key="community.id")
    author_id: str = Field(foreign_key="user.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.now)

    community: "Community" = Relationship(back_populates="posts")