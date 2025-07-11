# app/api/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import jwt_service

router = APIRouter()

@router.get("/me")
def get_current_user(token: dict = Depends(jwt_service.verify_token)):
    """
    Dummy route to verify token-based user session.
    Later, we can replace this with real user profile logic.
    """
    return {
        "user_id": token.get("sub"),
        "message": "User is authenticated",
    }