# import pytest
# from fastapi.testclient import TestClient
# from sqlmodel import SQLModel, create_engine, Session

# from app.main import app
# from app.core.config import settings
# from app.core.database import get_session

# # ✅ Use the database from .env (should point to lurnify_db)
# engine = create_engine(settings.database_url, echo=True)

# # ✅ Override the get_session dependency for testing
# def override_get_session():
#     with Session(engine) as session:
#         yield session

# app.dependency_overrides[get_session] = override_get_session
# client = TestClient(app)

# # ✅ Set up and tear down database tables for tests
# @pytest.fixture(autouse=True, scope="module")
# def create_test_db():
#     SQLModel.metadata.create_all(engine)
#     yield
#     SQLModel.metadata.drop_all(engine)


# def test_signup_and_login_with_password():
#     signup_payload = {
#         "email": "test@example.com",
#         "password": "securepass",
#         "username": "testuser"
#     }
#     res = client.post("/auth/signup", json=signup_payload)
#     assert res.status_code == 200
#     data = res.json()
#     assert data["email"] == "test@example.com"
#     assert data["auth_provider"] == "credentials"

#     login_payload = {
#         "email": "test@example.com",
#         "password": "securepass"
#     }
#     res = client.post("/auth/login", json=login_payload)
#     assert res.status_code == 200
#     data = res.json()
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"


# def test_signup_and_login_with_wallet():
#     signup_payload = {
#         "email": "wallet@example.com",
#         "wallet_address": "0xABC123456789abcdefABC123456789abcdef",
#         "username": "walletuser"
#     }
#     res = client.post("/auth/signup", json=signup_payload)
#     assert res.status_code == 200
#     data = res.json()
#     assert data["auth_provider"] == "web3"
#     assert data["wallet_address"] == "0xABC123456789abcdefABC123456789abcdef"

#     login_payload = {
#         "email": "wallet@example.com",
#         "wallet_address": "0xABC123456789abcdefABC123456789abcdef"
#     }
#     res = client.post("/auth/login", json=login_payload)
#     assert res.status_code == 200
#     data = res.json()
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"


# def test_protected_route_access():
#     email = "secure@example.com"
#     password = "pass123"

#     client.post("/auth/signup", json={"email": email, "password": password})
#     login_res = client.post("/auth/login", json={"email": email, "password": password})
#     token = login_res.json()["access_token"]

#     headers = {"Authorization": f"Bearer {token}"}
#     res = client.get("/auth/me", headers=headers)
#     assert res.status_code == 200
#     data = res.json()
#     assert data["email"] == email
#     assert data["auth_provider"] == "credentials"


# def test_protected_route_rejects_invalid_token():
#     headers = {"Authorization": "Bearer invalidtoken"}
#     res = client.get("/auth/me", headers=headers)
#     assert res.status_code == 401
#     assert res.json()["detail"] in ["Could not validate credentials", "Invalid token"]

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from app.main import app
from app.core.database import get_session
from app.models.user import User
from app.core.config import settings

# Use a separate Postgres DB for testing
DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL, echo=True)

# Override DB dependency with test session
def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

# Recreate test DB schema
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

def test_successful_signup():
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    response = client.post("/auth/signup", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == payload["email"]

def test_duplicate_signup():
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpass123"
    }
    response = client.post("/auth/signup", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"