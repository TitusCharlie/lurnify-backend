from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
import uuid

from app.models.course import Course
from app.models.community import Community


class CommunityCourseLink(SQLModel, table=True):
    community_id: str = Field(foreign_key="community.id", primary_key=True)
    course_id: str = Field(foreign_key="course.id", primary_key=True)


# Extend Community with relationship
Community.model_rebuild()  # ensure forward refs
Course.model_rebuild()


class Community(SQLModel, table=True):
    __tablename__ = "community"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    description: Optional[str] = None
    creator_id: str = Field(foreign_key="user.id")

    courses: List[Course] = Relationship(
        back_populates="communities",
        link_model=CommunityCourseLink
    )


class Course(SQLModel, table=True):
    __tablename__ = "course"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    description: Optional[str] = None
    creator_id: str = Field(foreign_key="user.id")

    communities: List[Community] = Relationship(
        back_populates="courses",
        link_model=CommunityCourseLink
    )