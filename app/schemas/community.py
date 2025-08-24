from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CommunityCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CommunityRead(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    creator_id: str

    class Config:
        from_attributes = True


class MembershipRead(BaseModel):
    id: str
    user_id: str
    community_id: str
    joined_at: datetime

    class Config:
        from_attributes = True


class PostCreate(BaseModel):
    content: str


class PostRead(BaseModel):
    id: str
    content: str
    created_at: datetime
    user_id: str
    community_id: str

    class Config:
        from_attributes = True
