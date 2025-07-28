from sqlmodel import Session, select
from fastapi import HTTPException
from app.schemas.auth import SignupRequest, AuthResponse, UserLogin
from app.models.user import User
from app.core.security import hash_password, create_access_token
import uuid
from typing import Optional
from app.services.utils import verify_password, create_jwt_token
from app.services.wallet import generate_wallet_address  # utility function

def signup_user(data: SignupRequest, db: Session) -> dict:
    existing = db.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate wallet address if not provided
    # wallet_address = SignupRequest.wallet_address or generate_wallet_address()

    user = User(    
        email=data.email,
        username=data.username,
        password_hash=hash_password(data.password) if data.password else None,
        # wallet_address=wallet_address,
        auth_provider="web3" if not data.password else "credentials"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id)})

    # return {"access_token": token, "token_type": "bearer"}
    return AuthResponse(
        access_token=token,
        token_type="bearer"
    )

def authenticate_user(data: dict, db: Session):
    if data.wallet_address:
        user = db.exec(select(User).where(User.wallet_address == data.wallet_address)).first()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid wallet address")
        return create_jwt_token(user)

    elif data.email and data.password:
        user = db.exec(select(User).where(User.email == data.email)).first()
        if not user or not user.password_hash or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return create_jwt_token(user)
    
    raise HTTPException(status_code=400, detail="Invalid login data")
