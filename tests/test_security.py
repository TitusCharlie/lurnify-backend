from app.core.security import hash_password, verify_password, jwt_service

def test_password_hashing_and_verification():
    raw = "testpassword"
    hashed = hash_password(raw)
    assert verify_password(raw, hashed)
    assert not verify_password("wrong", hashed)

def test_jwt_token_creation_and_verification():
    payload = {"sub": "user123"}
    token = jwt_service.create_access_token(payload)
    decoded = jwt_service.verify_token(token)
    assert decoded["sub"] == "user123"