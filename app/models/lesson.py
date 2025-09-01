# from sqlmodel import SQLModel, Field
# from typing import Optional
# from datetime import datetime
# import uuid

# class Lesson(SQLModel, table=True):
#     id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
#     module_id: str = Field(index=True, foreign_key="module.id")
#     title: str
#     description: Optional[str] = None
#     video_url: Optional[str] = None  # link to hosted video
#     duration_seconds: Optional[int] = None
#     creator_id: str = Field(index=True, foreign_key="user.id")
#     created_at: datetime = Field(default_factory=datetime.now)

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Lesson(SQLModel, table=True):
    id: str = Field(default_factory=generate_uuid, primary_key=True, index=True)
    title: str
    description: Optional[str] = None
    video_url: Optional[str] = None  # link to hosted video
    duration_seconds: Optional[int] = None

    module_id: str = Field(foreign_key="module.id")
    creator_id: str = Field(foreign_key="user.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    module: Optional["Module"] = Relationship(back_populates="lessons")