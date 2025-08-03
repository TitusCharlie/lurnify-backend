from sqlmodel import Session, select
from app.models.user import User
from app.schemas.auth import SignupRequest, AuthResponse
from app.schemas.user import UserRead
from app.core.security import hash_password, create_access_token

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
        hashed_password=hashed_pw,
        wallet_address=wallet
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id})

    return AuthResponse(
        access_token=token,
        user=UserRead.model_validate(user)
    )

def generate_wallet_address() -> str:
    # Simulate wallet generation (replace with actual logic)
    import uuid
    return f"solana-{uuid.uuid4().hex[:16]}"