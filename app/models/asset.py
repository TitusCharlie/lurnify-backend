from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from uuid import uuid4

class Asset(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    title: str
    description: Optional[str] = None
    course_id: str = Field(foreign_key="course.id")
    # Add relationships if needed
