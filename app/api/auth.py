from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.auth import SignupRequest, AuthResponse, UserLogin
from app.services.auth import signup_user, authenticate_user
from app.core.database import get_session

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# api/auth.py
@router.post("/signup", response_model=AuthResponse)
def signup(data: SignupRequest, db: Session = Depends(get_session)):
    return signup_user(data, db)

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_session)):
    token = authenticate_user(data.model_dump(), db)
    return {"access_token": token, "token_type": "bearer"}

# @router.post("/login", response_model=AuthResponse)
# def login(data: UserLogin, db: Session = Depends(get_session)):
#     user = db.exec(select(User).where(User.email == data.email)).first()
#     if not user:
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     if user.auth_provider == "credentials":
#         if not data.password (data.password, user.password_hash):
#             raise HTTPException(status_code=400, detail="Invalid password")
#     elif user.auth_provider == "web3":
#         if not data.wallet_address or data.wallet_address.lower() != user.wallet_address.lower():
#             raise HTTPException(status_code=400, detail="Invalid wallet")

#     token = jwt_service.create_access_token({"sub": user.id})
#     return {"access_token": token, "token_type": "bearer"}

# @router.get("/me", response_model=UserRead)
# def get_me(token: str = Depends(jwt_service.verify_token), db: Session = Depends(get_session)):
#     user_id = token.get("sub")
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     user = db.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user