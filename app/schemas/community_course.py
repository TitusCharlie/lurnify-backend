from pydantic import BaseModel
from typing import List, Optional


class CommunityCourseLinkRead(BaseModel):
    community_id: str
    course_id: str

    class Config:
        from_attributes = True


class CommunityWithCourses(BaseModel):
    id: str
    name: str
    description: Optional[str]
    courses: List["CourseRead"]

    class Config:
        from_attributes = True


class CourseWithCommunities(BaseModel):
    id: str
    title: str
    description: Optional[str]
    communities: List["CommunityRead"]

    class Config:
        from_attributes = True


# Avoid circular imports
from app.schemas.course import CourseRead
from app.schemas.community import CommunityRead
CommunityWithCourses.model_rebuild()
CourseWithCommunities.model_rebuild()
