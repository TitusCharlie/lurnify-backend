from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class Content(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    course_id: str = Field(foreign_key="course.id")
    type: str  # video | text | quiz | etc
    title: str
    body: Optional[str] = None  # markdown or text
    media_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    course: Optional[Course] = Relationship(back_populates="contents")