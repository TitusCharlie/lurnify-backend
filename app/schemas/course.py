from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    # tags: Optional[List[str]] = []
    thumbnail: Optional[HttpUrl] = None
    price: Optional[float] = 0.0
    level: Optional[str] = "beginner"
    language: Optional[str] = "English"

class CourseCreate(CourseBase):
    pass  # creator_id will be taken from the auth context

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    thumbnail: Optional[HttpUrl] = None
    price: Optional[float] = None
    is_published: Optional[bool] = None

class CourseRead(CourseBase):
    id: UUID
    slug: str
    author_id: UUID
    is_draft: bool
    is_published: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True