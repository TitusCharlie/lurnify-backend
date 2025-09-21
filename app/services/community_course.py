from sqlmodel import Session, select
from app.models.community_course import CommunityCourseLink
from app.models.community import Community
from app.models.course import Course


def link_course_to_community(course_id: str, community_id: str, db: Session):
    link = CommunityCourseLink(course_id=course_id, community_id=community_id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def unlink_course_from_community(course_id: str, community_id: str, db: Session):
    statement = select(CommunityCourseLink).where(
        CommunityCourseLink.course_id == course_id,
        CommunityCourseLink.community_id == community_id
    )
    link = db.exec(statement).first()
    if link:
        db.delete(link)
        db.commit()
    return link


def list_courses_for_community(community_id: str, db: Session):
    statement = select(Course).join(CommunityCourseLink).where(
        CommunityCourseLink.community_id == community_id
    )
    return db.exec(statement).all()


def list_communities_for_course(course_id: str, db: Session):
    statement = select(Community).join(CommunityCourseLink).where(
        CommunityCourseLink.course_id == course_id
    )
    return db.exec(statement).all()