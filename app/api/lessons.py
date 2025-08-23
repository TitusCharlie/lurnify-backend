from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.schemas.lesson import LessonCreate, LessonRead
from app.services.lesson import create_lesson, get_lesson, list_lessons, delete_lesson
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/modules/{module_id}/lessons", tags=["Lessons"])

@router.post("/", response_model=LessonRead)
def create_lesson_endpoint(module_id: str, data: LessonCreate, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return create_lesson(module_id, current_user.id, data, db)

@router.get("/", response_model=List[LessonRead])
def list_lessons_endpoint(module_id: str, db: Session = Depends(get_session)):
    return list_lessons(module_id, db)

@router.get("/{lesson_id}", response_model=LessonRead)
def get_lesson_endpoint(module_id: str, lesson_id: str, db: Session = Depends(get_session)):
    lesson = get_lesson(lesson_id, db)
    if not lesson or lesson.module_id != module_id:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@router.delete("/{lesson_id}")
def delete_lesson_endpoint(module_id: str, lesson_id: str, db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    lesson = get_lesson(lesson_id, db)
    if not lesson or lesson.module_id != module_id:
        raise HTTPException(status_code=404, detail="Lesson not found")
    if lesson.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return {"success": delete_lesson(lesson_id, db)}