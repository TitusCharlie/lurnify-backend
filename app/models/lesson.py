from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Lesson(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    module_id: str = Field(index=True, foreign_key="module.id")
    title: str
    description: Optional[str] = None
    video_url: Optional[str] = None  # link to hosted video
    duration_seconds: Optional[int] = None
    creator_id: str = Field(index=True, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)