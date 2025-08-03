# # content.py
# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional, TYPE_CHECKING
# from datetime import datetime, UTC
# import uuid

# if TYPE_CHECKING:
#     from app.models.course import Course

# class Content(SQLModel, table=True):
#     id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
#     title: str
#     body: str
#     course_id: str = Field(foreign_key="course.id")
#     created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

#     # course: Optional["Course"] = Relationship(back_populates="contents")  # ✅ Plain typing