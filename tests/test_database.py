# tests/test_database.py
import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.factory import create_app
from app.core.database import get_session
from fastapi.testclient import TestClient
import os
from dotenv import load_dotenv

def test_signup(client):
    response = client.post("/auth/signup", json={
        "email": "testuser@example.com",
        "password": "TestPass123",
        "username": "testuser"
    })
    print(response.json())

    assert response.status_code == 200 
    data = response.json()
    assert data["email"] == "testuser@example.com"
