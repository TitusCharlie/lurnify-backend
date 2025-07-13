# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from app.factory import create_app
from app.core.database import get_session

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/lurnify_db"
engine = create_engine(DATABASE_URL, echo=True)

# ✅ Correct session override: returns a generator function
def override_get_session():
    def _get_session():
        with Session(engine) as session:
            yield session
    return _get_session  # ✅ return the generator function, NOT the generator

# ✅ Setup test database schema
@pytest.fixture(scope="session", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    # SQLModel.metadata.drop_all(engine)  # Don't drop if using persistent test DB

# ✅ Test client that uses the override
@pytest.fixture
def client():
    app = create_app(get_session_override=override_get_session())  # ✅ Call the wrapper to get generator function
    return TestClient(app)