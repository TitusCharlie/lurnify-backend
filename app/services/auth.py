# #app/services/auth.py
# from fastapi import HTTPException, status
# from sqlmodel import Session, select

# from app.models.user import User
# from app.schemas.auth import SignupRequest, AuthResponse, UserLogin
# from app.schemas.user import UserRead
# from app.core.security import verify_password, hash_password, create_access_token

# import uuid


# def generate_wallet_address() -> str:
#     # Placeholder wallet generator (replace with Solana logic later)
#     return f"solana-{uuid.uuid4().hex[:16]}"


# def signup_user(data: SignupRequest, db: Session) -> AuthResponse:
#     # Check if user already exists
#     existing = db.exec(select(User).where(User.email == data.email)).first()
#     if existing:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="User with this email already exists"
#         )

#     hashed_pw = hash_password(data.password) if data.password else None
#     wallet = data.wallet_address or generate_wallet_address()

#     user = User(
#         email=data.email,
#         username=data.username,
#         hashed_password=hashed_pw,   # ✅ FIXED name
#         wallet_address=wallet,
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     token = create_access_token({"sub": str(user.id)})

#     return AuthResponse(
#         access_token=token,
#         token_type="bearer",   
#         user=UserRead.model_validate(user)
#     )


# def login_user(data: UserLogin, db: Session) -> AuthResponse:
#     user = db.exec(select(User).where(User.email == data.email)).first()

#     if not user or not user.hashed_password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     if not verify_password(data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Incorrect password")

#     token = create_access_token({"sub": user.id})

#     return AuthResponse(
#         access_token=token,
#         token_type="bearer", 
#         user=UserRead.model_validate(user)
#     )

from fastapi import HTTPException
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import UserLogin, AuthResponse
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
import uuid
from app.services.wallet import generate_wallet_address  # implement below

# ------------------ SIGNUP ------------------ #
def signup_user(data: UserCreate, db: Session) -> AuthResponse:
    existing_user = db.exec(select(User).where(User.email == data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(data.password)
    wallet = generate_wallet_address()

    new_user = User(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hashed_pw,
        wallet_address=wallet,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id), "email": new_user.email})

    return AuthResponse(
        access_token=token,
        user=UserRead.from_orm(new_user)
    )

# ------------------ LOGIN ------------------ #
def login_user(data: UserLogin, db: Session) -> AuthResponse:
    user = db.exec(select(User).where(User.email == data.email)).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id), "email": user.email})

    return AuthResponse(
        access_token=token,
        user=UserRead.from_orm(user)
    )