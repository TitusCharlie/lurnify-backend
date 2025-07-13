from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class JWTService:
    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

jwt_service = JWTService(
    secret_key=settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
    expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
