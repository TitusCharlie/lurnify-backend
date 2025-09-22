from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.community_course import CommunityCourseLinkRead
from app.services import community_course as service

router = APIRouter(prefix="/communities", tags=["Community-Courses"])

@router.post("/{community_id}/courses/{course_id}", response_model=CommunityCourseLinkRead)
async def add_course(community_id: str, course_id: str, session: AsyncSession = Depends(get_session)):
    try:
        return await service.add_course_to_community(session, community_id, course_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{community_id}/courses/{course_id}")
async def remove_course(community_id: str, course_id: str, session: AsyncSession = Depends(get_session)):
    try:
        await service.remove_course_from_community(session, community_id, course_id)
        return {"message": "Course removed from community"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{community_id}/courses", response_model=list[CommunityCourseLinkRead])
async def get_courses(community_id: str, session: AsyncSession = Depends(get_session)):
    return await service.list_courses_in_community(session, community_id)

@router.get("/courses/{course_id}/communities", response_model=list[CommunityCourseLinkRead])
async def get_communities(course_id: str, session: AsyncSession = Depends(get_session)):
    return await service.list_communities_for_course(session, course_id)