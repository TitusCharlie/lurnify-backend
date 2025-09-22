from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.community_course import CommunityCourseLink
from app.models.community import Community
from app.models.course import Course

# add course to community
async def add_course_to_community(session: AsyncSession, community_id: str, course_id: str) -> CommunityCourseLink:
    # ensure community exists
    result = await session.exec(select(Community).where(Community.id == community_id))
    community = result.first()
    if not community:
        raise ValueError("Community not found")

    # ensure course exists
    result = await session.exec(select(Course).where(Course.id == course_id))
    course = result.first()
    if not course:
        raise ValueError("Course not found")

    # prevent duplicates
    result = await session.exec(
        select(CommunityCourseLink).where(
            CommunityCourseLink.community_id == community_id,
            CommunityCourseLink.course_id == course_id
        )
    )
    existing = result.first()
    if existing:
        return existing

    link = CommunityCourseLink(community_id=community_id, course_id=course_id)
    session.add(link)
    await session.commit()
    await session.refresh(link)
    return link

# remove course from community
async def remove_course_from_community(session: AsyncSession, community_id: str, course_id: str) -> None:
    result = await session.exec(
        select(CommunityCourseLink).where(
            CommunityCourseLink.community_id == community_id,
            CommunityCourseLink.course_id == course_id
        )
    )
    link = result.first()
    if not link:
        raise ValueError("Link not found")
    await session.delete(link)
    await session.commit()

# list courses in a community
async def list_courses_in_community(session: AsyncSession, community_id: str):
    result = await session.exec(
        select(CommunityCourseLink).where(CommunityCourseLink.community_id == community_id)
    )
    return result.all()

# list communities a course belongs to
async def list_communities_for_course(session: AsyncSession, course_id: str):
    result = await session.exec(
        select(CommunityCourseLink).where(CommunityCourseLink.course_id == course_id)
    )
    return result.all()