import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app.models.user import User
from app.core.database import get_session
from app.core.security import hash_password

client = TestClient(app)

# === Fixture: Create a user once per module for auth-related tests ===
@pytest.fixture(scope="module", autouse=True)
def test_user():
    with Session(get_session()) as session:
        # Create a user directly in the database
        user = User(
            email="courseuser@example.com",
            username="courseuser",
            password=hash_password("coursepass"),
            auth_provider="credentials"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

# === Fixture: Login and return Authorization header ===
@pytest.fixture
def auth_header(test_user):
    login_res = client.post("/auth/login", json={
        "email": test_user.email,
        "password": "coursepass"
    })
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# === Test 1: Authenticated user can create a course and add content ===
def test_create_course_and_add_content(auth_header):
    course_payload = {
        "title": "Test Course",
        "description": "Test description",
        "thumbnail_url": "http://example.com/thumb.png"
    }

    # POST /courses/ to create course
    res = client.post("/courses/", json=course_payload, headers=auth_header)
    assert res.status_code == 200
    course = res.json()
    assert course["title"] == "Test Course"
    assert course["author_id"]

    # POST /courses/{course_id}/contents to add content
    content_payload = {
        "title": "Lesson 1",
        "body": "This is lesson content"
    }
    res = client.post(f"/courses/{course['id']}/contents", json=content_payload, headers=auth_header)
    assert res.status_code == 200
    content = res.json()
    assert content["title"] == "Lesson 1"
    assert content["course_id"] == course["id"]


# === Test 2: Anonymous users (unauthenticated) should get 401 on course creation ===
def test_unauthorized_course_creation():
    course_payload = {
        "title": "Unauthorized Course",
        "description": "You should not be able to do this"
    }

    # No auth headers → expect 401 Unauthorized
    res = client.post("/courses/", json=course_payload)
    assert res.status_code == 401


# === Test 3: Getting a course that doesn't exist should return 404 ===
def test_get_nonexistent_course(auth_header):
    # GET /courses/{invalid_id}
    res = client.get("/courses/invalid-id-1234", headers=auth_header)
    assert res.status_code == 404
    assert res.json()["detail"] == "Course not found"


# === Test 4: A new course should return an empty list of contents ===
def test_content_empty_list(auth_header):
    # Create new course
    course_payload = {
        "title": "Empty Course",
        "description": "Should have no content"
    }
    res = client.post("/courses/", json=course_payload, headers=auth_header)
    assert res.status_code == 200
    course_id = res.json()["id"]

    # GET /courses/{course_id}/contents should return []
    res = client.get(f"/courses/{course_id}/contents", headers=auth_header)
    assert res.status_code == 200
    assert res.json() == []