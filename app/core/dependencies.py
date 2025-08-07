# app.core.dependencies.py

from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import verify_access_token
from app.models.user import User
from sqlmodel import select

def get_current_user(
    token: str = Depends(verify_access_token), 
    db: Session = Depends(get_session)
) -> User:
    user = db.exec(select(User).where(User.id == token.sub)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
