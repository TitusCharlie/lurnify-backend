# app/models/module.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class Module(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    course_id: str = Field(foreign_key="course.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # course: "Course" = Relationship(back_populates="modules")
    # lessons: List["Lesson"] = Relationship(back_populates="module")