import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import SQLModel, Session
from app.core.database import get_session, engine
from app.models.user import User
from app.core.security import hash_password

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

def get_token():
    email = "instructor@example.com"
    password = "testpass"
    client.post("/auth/signup", json={"email": email, "password": password})
    res = client.post("/auth/login", json={"email": email, "password": password})
    return res.json()["access_token"]

def test_create_course_and_add_content():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Create course
    course_data = {
        "title": "Intro to Solidity",
        "description": "Learn Ethereum smart contracts",
        "thumbnail_url": "https://example.com/image.png"
    }
    res = client.post("/courses/", json=course_data, headers=headers)
    assert res.status_code == 200
    course = res.json()
    assert course["title"] == "Intro to Solidity"
    course_id = course["id"]

    # List courses
    res = client.get("/courses/")
    assert res.status_code == 200
    assert any(c["id"] == course_id for c in res.json())

    # Get course by ID
    res = client.get(f"/courses/{course_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Intro to Solidity"

    # Add content to course
    content_data = {
        "type": "video",
        "title": "Getting Started with Remix",
        "body": "This video explains basic Remix usage.",
        "media_url": "https://ipfs.io/ipfs/Qm123abc"
    }
    res = client.post(f"/courses/{course_id}/contents", json=content_data, headers=headers)
    assert res.status_code == 200
    content = res.json()
    assert content["title"] == "Getting Started with Remix"

    # Get all contents for course
    res = client.get(f"/courses/{course_id}/contents")
    assert res.status_code == 200
    contents = res.json()
    assert len(contents) == 1
    assert contents[0]["type"] == "video"

def test_unauthorized_course_creation():
    course_data = {
        "title": "Web3 Security",
        "description": "Learn about smart contract security.",
        "thumbnail_url": "https://example.com/security.png"
    }
    res = client.post("/courses/", json=course_data)
    assert res.status_code == 401

def test_get_nonexistent_course():
    res = client.get("/courses/invalid-id")
    assert res.status_code == 404
    assert res.json()["detail"] == "Course not found"

def test_content_empty_list():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Create course
    course_data = {
        "title": "Zero Content Course",
        "description": "Testing empty content.",
        "thumbnail_url": "https://example.com/none.png"
    }
    res = client.post("/courses/", json=course_data, headers=headers)
    assert res.status_code == 200
    course_id = res.json()["id"]

    # Fetch contents (should be empty)
    res = client.get(f"/courses/{course_id}/contents")
    assert res.status_code == 200
    assert res.json() == []