# from datetime import datetime, timedelta, UTC
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from typing import Optional
# from app.core.config import settings
# from fastapi import HTTPException, status, Depends
# from app.models.token import TokenData  # define this Pydantic model
# from fastapi.security import OAuth2PasswordBearer
# # from dotenv import load_dotenv
# import os

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# class JWTService:
#     def __init__(self, secret_key: str, algorithm: str, expire_minutes: int):
#         self.secret_key = secret_key
#         self.algorithm = algorithm
#         self.expire_minutes = expire_minutes

#     def create_access_token(self, data: dict) -> str:
#         to_encode = data.copy()
#         expire = datetime.now(UTC) + timedelta(minutes=self.expire_minutes)
#         to_encode.update({"exp": expire})
#         return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

#     def verify_token(self, token: str) -> Optional[dict]:
#         try:
#             payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
#             return payload
#         except JWTError:
#             return None

# jwt_service = JWTService(
#     secret_key=settings.SECRET_KEY,
#     algorithm=settings.ALGORITHM,
#     expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
# )

# # -----------------------
# # Password utilities
# # -----------------------
# def hash_password(password: str) -> str:
#     return pwd_context.hash(password)


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# # -----------------------
# # JWT utilities
# # -----------------------
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
#     to_encode = data.copy()
#     expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     return encoded_jwt

# def verify_access_token(token: str = Depends(oauth2_scheme)) -> TokenData:
#     """Dependency for protected routes (extracts user_id from JWT)"""
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         return TokenData(sub=user_id)
#     except JWTError:
#         raise credentials_exception

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from app.models.user import User
from app.core.database import get_session
import os

# JWT config
SECRET_KEY = os.getenv("JWT_SECRET", "secret_lurnify_key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-swagger")

# ------------------ PASSWORD UTILS ------------------ #
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ------------------ JWT UTILS ------------------ #
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# ------------------ CURRENT USER ------------------ #
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session),
):
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
