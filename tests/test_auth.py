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
    # SQLModel.metadata.drop_all(engine)

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