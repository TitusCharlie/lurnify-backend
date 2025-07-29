from sqlmodel import Session, select
from fastapi import HTTPException
from app.schemas.auth import SignupRequest, AuthResponse, UserLogin
from app.models.user import User
from app.core.security import hash_password, create_access_token
import uuid
from typing import Optional
from app.services.utils import verify_password, create_jwt_token
from app.services.wallet import generate_wallet_address  # utility 

# app/services/auth.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlmodel import select
from app.models.user import User
from app.core.database import get_session
from app.core.config import settings


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
        token_type="bearer",
        user=user
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_session)
# ) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = db.exec(select(User).where(User.id == user_id)).first()
#     if user is None:
#         raise credentials_exception
#     return user
