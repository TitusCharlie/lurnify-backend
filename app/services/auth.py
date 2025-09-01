# from fastapi import HTTPException
# from sqlmodel import Session, select
# from app.models.user import User
# from app.schemas.auth import SignupRequest, AuthResponse, UserLogin
# from app.schemas.user import UserRead
# from app.core.security import verify_password, hash_password, create_access_token

# def signup_user(data: SignupRequest, db: Session) -> AuthResponse:
#     # Check if user already exists
#     existing = db.exec(select(User).where(User.email == data.email)).first()
#     if existing:
#         raise ValueError("User already exists")

#     hashed_pw = hash_password(data.password) if data.password else None
#     wallet = data.wallet_address or generate_wallet_address()

#     user = User(
#         email=data.email,
#         username=data.username,
#         password_hash=hashed_pw,
#         wallet_address=wallet
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     token = create_access_token({"sub": user.id})

#     return AuthResponse(
#         access_token=token,
#         user=UserRead.model_validate(user)
#     )

# def generate_wallet_address() -> str:
#     pass
#     # Simulate wallet generation (replace with actual logic)
#     # import uuid
#     # return f"solana-{uuid.uuid4().hex[:16]}"

# def login_user(data: UserLogin, db: Session) -> AuthResponse:
#     user = db.exec(select(User).where(User.email == data.email)).first()

#     if not user or not user.password_hash:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     if not verify_password(data.password, user.password_hash):
#         raise HTTPException(status_code=401, detail="Incorrect password")

#     token = create_access_token({"sub": user.id})

#     return AuthResponse(
#         access_token=token,
#         user=UserRead.model_validate(user)
#     )

from fastapi import HTTPException
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
        raise ValueError("User already exists")

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

    token = create_access_token({"sub": user.id})

    return AuthResponse(
        access_token=token,
        user=UserRead.model_validate(user)
    )


def login_user(data: UserLogin, db: Session) -> AuthResponse:
    user = db.exec(select(User).where(User.email == data.email)).first()

    if not user or not user.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_access_token({"sub": user.id})

    return AuthResponse(
        access_token=token,
        user=UserRead.model_validate(user)
    )