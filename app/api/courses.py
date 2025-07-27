#app/api/courses.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.models.course import Course
from app.models.content import Content
from app.schemas.course import CourseCreate, CourseRead
from app.schemas.content import ContentCreate, ContentRead
from app.core.database import get_session
from app.core.security import jwt_service

router = APIRouter()

@router.post("/courses/", response_model=CourseRead)
def create_course(data: CourseCreate, db: Session = Depends(get_session), token: dict = Depends(jwt_service.verify_token)):
    author_id = token.get("sub")
    course = Course(**data.dict(), author_id=author_id)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("/courses/", response_model=List[CourseRead])
def list_courses(db: Session = Depends(get_session)):
    return db.exec(select(Course)).all()

@router.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: str, db: Session = Depends(get_session)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/courses/{course_id}/contents", response_model=ContentRead)
def add_content(course_id: str, data: ContentCreate, db: Session = Depends(get_session), token: dict = Depends(jwt_service.verify_token)):
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    content = Content(**data.dict(), course_id=course_id)
    db.add(content)
    db.commit()
    db.refresh(content)
    return content

@router.get("/courses/{course_id}/contents", response_model=List[ContentRead])
def list_contents(course_id: str, db: Session = Depends(get_session)):
    return db.exec(select(Content).where(Content.course_id == course_id)).all()