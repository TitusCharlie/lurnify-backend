from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserRead
from app.core.database import get_session
from app.core.security import hash_password, verify_password, jwt_service

router = APIRouter()

@router.post("/signup", response_model=UserRead)
def signup(data: UserCreate, db: Session = Depends(get_session)):
    existing = db.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=data.email,
        username=data.username,
        wallet_address=data.wallet_address,
        password_hash=hash_password(data.password) if data.password else None,
        auth_provider="web3" if data.wallet_address else "credentials",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.email == data.email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if user.auth_provider == "credentials":
        if not data.password or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid password")
    elif user.auth_provider == "web3":
        if not data.wallet_address or data.wallet_address.lower() != user.wallet_address.lower():
            raise HTTPException(status_code=400, detail="Invalid wallet")

    token = jwt_service.create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
def get_me(token: str = Depends(jwt_service.verify_token), db: Session = Depends(get_session)):
    user_id = token.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user