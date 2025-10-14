# app/dependencies.py
from fastapi import Depends, HTTPException, status
from app.core.security import jwt_service, oauth2_scheme
from app.models.user import User
from app.core.database import get_session
from sqlmodel import select

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_session)):
    """
    Extract token from Authorization header and verify user session.
    """
    payload = jwt_service.verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
