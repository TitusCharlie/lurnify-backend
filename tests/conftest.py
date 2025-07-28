# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from app.factory import create_app
from app.core.database import get_session
import os
from dotenv import load_dotenv
from pathlib import Path
from app.core.config import settings

print("DATABASE_URL =", settings.database_url)


# # Explicitly load .env.test
# env_path = Path(__file__).parent.parent / ".env.test"
# load_dotenv(dotenv_path=env_path)
# # Print the database URL
# print("DATABASE_URL =", os.getenv("DATABASE_URL"))
# # ✅ Load test environment
# load_dotenv(".env.test", override=True)
DATABASE_URL = settings.database_url

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Did you forget to create or load .env.test?")

engine = create_engine(DATABASE_URL, echo=True)

# Correct session override: returns a generator function
def override_get_session():
    def _get_session():
        with Session(engine) as session:
            yield session
    return _get_session  # return the generator function, NOT the generator

# Setup test database schema
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    # SQLModel.metadata.drop_all(engine)
    
# Test client that uses the override
@pytest.fixture
def client():
    app = create_app(get_session_override=override_get_session())  # Call the wrapper to get generator function
    return TestClient(app)
