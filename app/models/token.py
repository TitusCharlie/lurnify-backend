# app/models/token.py

from pydantic import BaseModel

class TokenData(BaseModel):
    sub: str  # user id from JWT "sub" claim
