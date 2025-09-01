# from datetime import datetime
# from typing import Optional
# from sqlmodel import Field, Relationship, SQLModel
# from app.models.course import Course

# class Module(SQLModel, table=True):
#     id: Optional[str] = Field(default=None, primary_key=True)
#     title: str
#     description: Optional[str] = None
#     order: Optional[int] = None
#     course_id: str = Field(foreign_key="course.id")
#     created_at: datetime = Field(default_factory=datetime.now)
#     updated_at: datetime = Field(default_factory=datetime.now)
#     is_published: bool = Field(default=False)

#     course: Optional[Course] = Relationship(back_populates="modules")

from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
import uuid

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Module(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    title: str
    description: Optional[str] = None
    order: Optional[int] = None
    is_published: bool = Field(default=False)

    course_id: str = Field(foreign_key="course.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    course: Optional["Course"] = Relationship(back_populates="modules")
    lessons: List["Lesson"] = Relationship(back_populates="module")
from app.models import Lesson
from app.models import Course
