# app/models/lesson.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class Lesson(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    content: Optional[str] = None
    video_url: Optional[str] = None
    module_id: str = Field(foreign_key="module.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # module: "Module" = Relationship(back_populates="lessons")