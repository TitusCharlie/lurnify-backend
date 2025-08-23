from sqlmodel import Session, select
from typing import Optional, List
from app.models.lesson import Lesson
from app.schemas.lesson import LessonCreate

def create_lesson(module_id: str, creator_id: str, data: LessonCreate, db: Session) -> Lesson:
    lesson = Lesson(**data.dict(), module_id=module_id, creator_id=creator_id)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return lesson

def get_lesson(lesson_id: str, db: Session) -> Optional[Lesson]:
    return db.get(Lesson, lesson_id)

def list_lessons(module_id: str, db: Session) -> List[Lesson]:
    return db.exec(select(Lesson).where(Lesson.module_id == module_id)).all()

def delete_lesson(lesson_id: str, db: Session) -> bool:
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        return False
    db.delete(lesson)
    db.commit()
    return True