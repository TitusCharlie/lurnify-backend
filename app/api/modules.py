from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.core.database import get_session
from app.schemas.module import ModuleCreate, ModuleRead, ModuleUpdate
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.module import (
    publish_module,
    create_module,
    get_modules_for_course,
    delete_module,
    update_module
)

router = APIRouter(prefix="/courses/{course_id}/modules", tags=["Modules"])


@router.post("/", response_model=ModuleRead)
def create_module_api(course_id: int, module_data: ModuleCreate, 
                  session: Session = Depends(get_session), 
                  current_user: User = Depends(get_current_user)):
    return create_module(session, course_id, current_user.id, module_data)

@router.put("/{module_id}/publish", response_model=ModuleRead)
def publish_module_api(course_id: int, module_id: int,
            db: Session = Depends(get_session),
            current_user: User = Depends(get_current_user)):
    published = publish_module(course_id, module_id, current_user.id, db)
    if not published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed or module/course not found"
        )
    return published

@router.get("/", response_model=List[ModuleRead])
def list_modules_api(course_id: int, session: Session = Depends(get_session)):
    return get_modules_for_course(session, course_id)


@router.put("/{module_id}", response_model=ModuleRead)
def update_module_api(course_id: int, module_id: int, update_data: ModuleUpdate,
                  session: Session = Depends(get_session),
                  current_user: User = Depends(get_current_user)):
    return update_module(session, module_id, current_user.id, update_data)


@router.delete("/{module_id}")
def delete_module_api(course_id: int, module_id: int,
                  session: Session = Depends(get_session),
                  current_user: User = Depends(get_current_user)):
    return delete_module(session, module_id, current_user.id)
