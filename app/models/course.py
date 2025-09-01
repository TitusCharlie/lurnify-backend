# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional, List
# from datetime import datetime, UTC
# import uuid

# class Course(SQLModel, table=True):
#     id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, index=True)
#     title: str
#     slug: str = Field(index=True, unique=True)
#     description: Optional[str] = None
#     category: Optional[str] = Field(default=None, index=True)
#     price: Optional[float] = 0.0
#     thumbnail_url: Optional[str] = None
#     # tags: Optional[List[str]] = Field(default_factory=list, sa_column_kwargs={"nullable": True})
#     level: Optional[str] = "beginner"  # beginner | intermediate | advanced
#     language: Optional[str] = "English"

#     is_published: bool = Field(default=False)
#     is_draft: bool = Field(default=True)
#     author_id: Optional[str] = Field(foreign_key="user.id")

#     created_at: datetime = Field(default_factory=datetime.now)
#     updated_at: datetime = Field(default_factory=datetime.now)

#     # lessons: List["Lesson"] = Relationship(back_populates="course")  # later

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Course(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    title: str
    slug: str = Field(index=True, unique=True)
    description: Optional[str] = None
    category: Optional[str] = Field(default=None, index=True)
    price: Optional[float] = 0.0
    thumbnail_url: Optional[str] = None
    level: Optional[str] = "beginner"  # beginner | intermediate | advanced
    language: Optional[str] = "English"

    is_published: bool = Field(default=False)
    is_draft: bool = Field(default=True)

    author_id: str = Field(foreign_key="user.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    modules: List["Module"] = Relationship(back_populates="course")