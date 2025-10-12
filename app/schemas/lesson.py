from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class LessonCreate(BaseModel):
    title: str
    description: Optional[str] = None
    video_url: Optional[HttpUrl] = None
    duration_seconds: Optional[int] = None

class LessonRead(LessonCreate):
    id: str
    module_id: str
    creator_id: str
    created_at: datetime

    class Config:
        from_attributes = True