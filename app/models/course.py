# course.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, UTC
import uuid

if TYPE_CHECKING:
    from app.models.content import Content

class Course(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    description: Optional[str] = None
    author_id: str = Field(foreign_key="user.id")
    thumbnail_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    # published: bool = Field(default=False, description="Weather the course is published")

    contents: List["Content"] = Relationship(back_populates="course")  # ✅ Don't use Mapped here