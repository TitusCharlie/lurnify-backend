from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ContentCreate(BaseModel):
    type: str
    title: str
    body: Optional[str] = None
    media_url: Optional[str] = None

class ContentRead(BaseModel):
    id: str
    type: str
    title: str
    body: Optional[str]
    media_url: Optional[str]
    course_id: str
    created_at: datetime