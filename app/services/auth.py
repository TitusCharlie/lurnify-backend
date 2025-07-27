from sqlmodel import Session, select
from fastapi import HTTPException
from app.schemas.auth import SignupRequest, AuthResponse
from app.models.user import User
# from app.core.security import hash_password, create_access_token
# from app.services.wallet_service import generate_wallet  # optional
import uuid


def signup_user(data: SignupRequest, db: Session) -> AuthResponse:
    # 1. Check if user already exists
    existing_user = db.exec(select(User).where(User.email == data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash password
    hashed_pw = hash_password(data.password)

    # 3. Generate wallet
    wallet_address = generate_wallet()  # or stub like: str(uuid.uuid4())

    # 4. Create user
    user = User(
        email=data.email,
        username=data.username,
        password_hash=hashed_pw,
        wallet_address=wallet_address,
        auth_provider="credentials"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 5. Create JWT token
    token = create_access_token({"sub": user.id})

    # 6. Return response
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=user
    )