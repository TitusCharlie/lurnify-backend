# app/api/users.py

# from fastapi import APIRouter, Depends, HTTPException, status
# from app.core.security import jwt_service

# router = APIRouter()

# @router.get("/me")
# def get_current_user(token: dict = Depends(jwt_service.verify_token)):
#     """
#     Dummy route to verify token-based user session.
#     Later, we can replace this with real user profile logic.
#     """
#     return {
#         "user_id": token.get("sub"),
#         "message": "User is authenticated",
#     }

# app/api/user.py
from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        # "username": current_user.username,
        "wallet_address": current_user.wallet_address,
        "message": "User is authenticated",
    }
