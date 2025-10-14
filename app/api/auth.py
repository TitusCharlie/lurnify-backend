# # api/auth.py
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlmodel import Session, select
# from app.models.user import User
# from app.schemas.auth import SignupRequest, AuthResponse, UserLogin
# from app.services.auth import signup_user, login_user
# from app.core.database import get_session
# from fastapi.security import OAuth2PasswordRequestForm

# router = APIRouter(
#     prefix="/auth",
#     tags=["auth"]
# )

# @router.post("/signup", response_model=AuthResponse)
# def signup(data: SignupRequest, db: Session = Depends(get_session)):
#     try:
#         return signup_user(data, db)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # @router.post("/login", response_model=AuthResponse)
# # def login(data: UserLogin, db: Session = Depends(get_session)):
# #     return login_user(data, db)

# # -------------------------
# # LOGIN ROUTE (HYBRID)
# # -------------------------
# @router.post("/login", response_model=AuthResponse)
# def login(
#     db: Session = Depends(get_session),
#     form_data: OAuth2PasswordRequestForm = Depends(None),
#     json_data: UserLogin | None = None
# ):
#     """
#     Login either via:
#     - Swagger UI (form-data, using username/password)
#     - Frontend (JSON: { "email": "...", "password": "..." })
#     """
#     # Swagger login (form)
#     if form_data:
#         json_data = UserLogin(email=form_data.username, password=form_data.password)

#     if not json_data:
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail="Missing credentials"
#         )

#     return login_user(json_data, db)

# # @router.post("/login", response_model=AuthResponse)
# # def login(data: UserLogin, db: Session = Depends(get_session)):
# #     user = db.exec(select(User).where(User.email == data.email)).first()
# #     if not user:
# #         raise HTTPException(status_code=400, detail="Invalid credentials")

# #     if user.auth_provider == "credentials":
# #         if not data.password (data.password, user.password_hash):
# #             raise HTTPException(status_code=400, detail="Invalid password")
# #     elif user.auth_provider == "web3":
# #         if not data.wallet_address or data.wallet_address.lower() != user.wallet_address.lower():
# #             raise HTTPException(status_code=400, detail="Invalid wallet")

# #     token = jwt_service.create_access_token({"sub": user.id})
# #     return {"access_token": token, "token_type": "bearer"}

# # @router.get("/me", response_model=UserRead)
# # def get_me(token: str = Depends(jwt_service.verify_token), db: Session = Depends(get_session)):
# #     user_id = token.get("sub")
# #     if not user_id:
# #         raise HTTPException(status_code=401, detail="Invalid token")
# #     user = db.get(User, user_id)
# #     if not user:
# #         raise HTTPException(status_code=404, detail="User not found")
# #     return user


from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.schemas.user import UserCreate, UserRead
from app.schemas.auth import UserLogin, AuthResponse
from app.services.auth import signup_user, login_user
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", response_model=AuthResponse)
def signup(data: UserCreate, db: Session = Depends(get_session)):
    return signup_user(data, db)

# ✅ Standard JSON login (for frontend API calls)
@router.post("/login", response_model=AuthResponse)
def login(data: UserLogin, db: Session = Depends(get_session)):
    return login_user(data, db)

# ✅ Swagger-compatible login (form-data: username + password)
@router.post("/login-swagger", response_model=AuthResponse, include_in_schema=False)
def login_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    # Map username → email
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    return login_user(credentials, db)

@router.get("/me", response_model=UserRead)
def get_me(current_user: UserRead = Depends(get_current_user)):
    return current_user