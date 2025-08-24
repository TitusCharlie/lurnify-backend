from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from app.models.course import Course

class Module(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    order: Optional[int] = None
    course_id: str = Field(foreign_key="Course.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_published: bool = Field(default=False)

    course: Optional[Course] = Relationship(back_populates="modules")