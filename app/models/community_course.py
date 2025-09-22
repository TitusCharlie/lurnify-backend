from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from uuid import uuid4

class CommunityCourseLink(SQLModel, table=True):
    __tablename__ = "community_course_link"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True, index=True)

    community_id: str = Field(foreign_key="community.id", nullable=False)
    course_id: str = Field(foreign_key="course.id", nullable=False)

    created_at: datetime = Field(default_factory=datetime.now)

    # relationships (for navigation if needed)
    community: Optional["Community"] = Relationship(back_populates="courses")
    course: Optional["Course"] = Relationship(back_populates="communities")
