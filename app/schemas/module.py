from typing import Optional
from sqlmodel import SQLModel

class ModuleBase(SQLModel):
    title: str
    description: Optional[str] = None
    order: Optional[int] = None

class ModuleCreate(ModuleBase):
    pass

class ModuleRead(ModuleBase):
    id: int
    course_id: int

class ModuleUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    is_published: Optional[bool] = None