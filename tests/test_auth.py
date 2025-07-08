import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import Session
from app.core.database import get_session, engine
from app.models.user import User
from app.core.security import hash_password

client = TestClient(app)

@pytest.fixture(autouse=True)
def create_test_db():
    User.metadata.create_all(engine)
    yield
    User.metadata.drop_all(engine)

def test_signup_and_login_with_password():
    signup_payload = {
        "email": "test@example.com",
        "password": "securepass",
        "username": "testuser"
    }
    res = client.post("/auth/signup", json=signup_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == "test@example.com"
    assert data["auth_provider"] == "credentials"

    login_payload = {
        "email": "test@example.com",
        "password": "securepass"
    }
    res = client.post("/auth/login", json=login_payload)
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_signup_and_login_with_wallet():
    signup_payload = {
        "email": "wallet@example.com",
        "wallet_address": "0xABC123456789abcdef",
        "username": "walletuser"
    }
    res = client.post("/auth/signup", json=signup_payload)
    assert res.status_code == 200
    assert res.json()["auth_provider"] == "web3"

    login_payload = {
        "email": "wallet@example.com",
        "wallet_address": "0xABC123456789abcdef"
    }
    res = client.post("/auth/login", json=login_payload)
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_protected_route_access():
    signup = client.post("/auth/signup", json={
        "email": "me@example.com",
        "password": "12345678"
    })
    token = client.post("/auth/login", json={
        "email": "me@example.com",
        "password": "12345678"
    }).json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res = client.get("/auth/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["email"] == "me@example.com"