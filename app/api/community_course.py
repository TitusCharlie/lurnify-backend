from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.services import community_course as service
from app.schemas.community_course import (
    CommunityCourseLinkRead,
    CommunityWithCourses,
    CourseWithCommunities
)
from app.services.auth import get_current_user


router = APIRouter(
    prefix="/community-courses",
    tags=["Community-Courses"]
)


@router.post("/{community_id}/add/{course_id}", response_model=CommunityCourseLinkRead)
def link_course(
    community_id: str,
    course_id: str,
    db: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    return service.link_course_to_community(course_id, community_id, db)


@router.delete("/{community_id}/remove/{course_id}", response_model=CommunityCourseLinkRead)
def unlink_course(
    community_id: str,
    course_id: str,
    db: Session = Depends(get_session),
    user=Depends(get_current_user)
):
    link = service.unlink_course_from_community(course_id, community_id, db)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@router.get("/{community_id}/courses", response_model=List[CourseWithCommunities])
def list_courses(community_id: str, db: Session = Depends(get_session)):
    return service.list_courses_for_community(community_id, db)


@router.get("/courses/{course_id}/communities", response_model=List[CommunityWithCourses])
def list_communities(course_id: str, db: Session = Depends(get_session)):
    return service.list_communities_for_course(course_id, db)