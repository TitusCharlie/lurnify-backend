from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.auth import SignupRequest, AuthResponse, UserLogin
from app.schemas.user import UserRead
from app.core.security import verify_password, hash_password, create_access_token

import uuid


def generate_wallet_address() -> str:
    # Placeholder wallet generator (replace with Solana logic later)
    return f"solana-{uuid.uuid4().hex[:16]}"


def signup_user(data: SignupRequest, db: Session) -> AuthResponse:
    # Check if user already exists
    existing = db.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    hashed_pw = hash_password(data.password) if data.password else None
    wallet = data.wallet_address or generate_wallet_address()

    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hashed_pw,   # ✅ FIXED name
        wallet_address=wallet,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})

    return AuthResponse(
        access_token=token,
        token_type="bearer",   
        user=UserRead.model_validate(user)
    )


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

def login_user(data: UserLogin, db: Session) -> AuthResponse:
    # --- Temporary bcrypt check (to debug Render issue) ---
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    import bcrypt
    try:
        version = getattr(bcrypt, "__about__", None)
        print("✅ Using bcrypt:", version or "missing __about__")
    except Exception as e:
        print("⚠️ bcrypt check failed:", e)
    # ------------------------------------------------------

    user = db.exec(select(User).where(User.email == data.email)).first()

    if not user or not user.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({"sub": user.id})

    return AuthResponse(
        access_token=token,
        token_type="bearer", 
        user=UserRead.model_validate(user)
    )
