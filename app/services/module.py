from sqlmodel import Session, select
from typing import Optional, List
from fastapi import HTTPException, status
from app.models.module import Module
from app.schemas.module import ModuleCreate, ModuleUpdate
from app.models.course import Course


def create_module(session: Session, course_id: int, author_id: int, module_data: ModuleCreate) -> Module:
    module_dict = module_data.model_dump()
    # Check course ownership
    course = session.exec(select(Course).where(Course.id == course_id)).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    if course.author_id != author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your course")

    new_module = Module(**module_dict, course_id=course_id)
    session.add(new_module)
    session.commit()
    session.refresh(new_module)
    return new_module

def publish_module(course_id: int, module_id: int, current_user_id: str, db: Session) -> Optional[Module]:
    # Verify that the course exists and belongs to current user
    course = db.get(Course, course_id)
    if not course or course.author_id != current_user_id:
        return None

    module = db.get(Module, module_id)
    if not module or module.course_id != course_id:
        return None

    module.is_published = True
    db.commit()
    db.refresh(module)
    return module

def get_modules_for_course(session: Session, course_id: int) -> List[Module]:
    return session.exec(select(Module).where(Module.course_id == course_id).order_by(Module.order)).all()


def update_module(session: Session, module_id: int, author_id: int, update_data: ModuleUpdate) -> Module:
    module = session.get(Module, module_id)
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    if module.course.author_id != author_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your module")

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(module, field, value)

    session.add(module)
    session.commit()
    session.refresh(module)
    return module


def delete_module(session: Session, module_id: int, creator_id: int):
    module = session.get(Module, module_id)
    if not module:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Module not found")
    if module.course.author_id != creator_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not your module")

    session.delete(module)
    session.commit()
    return {"message": "Module deleted"}