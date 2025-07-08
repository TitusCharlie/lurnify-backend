from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None

class CourseRead(BaseModel):
    id: str
    title: str
    description: Optional[str]
    thumbnail_url: Optional[str]
    author_id: str
    created_at: datetime