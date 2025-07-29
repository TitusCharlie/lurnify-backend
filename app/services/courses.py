# app/services/courses.py

from sqlmodel import Session
from app.models.course import Course
from app.schemas.course import CourseCreate

def create_course(data: CourseCreate, creator_id: str, db: Session) -> Course:
    course = Course(**data.dict(), creator_id=creator_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
