from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseRead, CourseUpdate
from app.services.courses import (
    create_course,
    get_course,
    list_courses,
    update_course,
    delete_course,
    publish_course
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

# Simulate a user until auth is fully ready
FAKE_USER = User(id="wrong-user-id", email="wrong@example.com", username="WrongDevUser")
FAKE_USER_1 = User(id="right-user-id", email="right@example.com", username="RightDevUser")

@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course_api(
    data: CourseCreate,
    db: Session = Depends(get_session),
    current_user: User = FAKE_USER,
):
    return create_course(data,
                         author_id=current_user.id,
                         db=db
                         )

@router.put("/{course_id}/publish", response_model=CourseRead)
def publish(course_id: str, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    published = publish_course(course_id, current_user.id, db)
    if not published:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed or course not found")
    return published

@router.get("/", response_model=List[CourseRead])
def list_courses_api(db: Session = Depends(get_session)):
    return list_courses(db)


@router.get("/{course_id}", response_model=CourseRead)
def get_course_api(course_id: str, db: Session = Depends(get_session)):
    course = get_course(course_id, db)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.put("/{course_id}", response_model=CourseRead)
def update_course_api(
    course_id: str,
    data: CourseUpdate,
    db: Session = Depends(get_session),
    current_user_id: User = FAKE_USER.id,
):
    course = update_course(course_id, data, db, current_user_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course_api(
    course_id: str,
    db: Session = Depends(get_session),
    current_user_id: User = FAKE_USER.id,
):
    success = delete_course(course_id, db, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Course not found")