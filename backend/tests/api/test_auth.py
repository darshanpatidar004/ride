import pytest
from fastapi.testclient import TestClient

def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Ride Booking Platform API"}

def test_signup_user(client: TestClient):
    data = {
        "email": "test@example.com",
        "phone_number": "1234567890",
        "password": "testpassword",
        "full_name": "Test User",
        "role": "CUSTOMER"
    }
    response = client.post("/api/v1/auth/signup", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == data["email"]
    assert "id" in response.json()

def test_login_user(client: TestClient):
    # Depends on test_signup_user having run
    data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login/access-token", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
