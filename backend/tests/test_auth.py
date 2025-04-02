import pytest
from fastapi.testclient import TestClient
import os
import json
from app.main import app
from app.services.auth import AuthService
from app.schemas.user import UserCreate

client = TestClient(app)


@pytest.fixture
def test_user_data():
    """Fixture for test user data"""
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123",
        "role": "adopter",
        "full_name": "Test User"
    }


class MockSupabaseResponse:
    """Mock response for Supabase operations"""
    def __init__(self, success=True, user=None):
        self.success = success
        self.user = user or {
            "id": "test-user-id",
            "email": "testuser@example.com",
            "created_at": "2025-04-01T00:00:00Z",
            "user_metadata": {
                "username": "testuser",
                "role": "adopter",
                "full_name": "Test User"
            },
            "confirmed_at": "2025-04-01T00:00:00Z"
        }


# Mock the Supabase methods to avoid actual API calls during tests
def mock_sign_up(*args, **kwargs):
    return MockSupabaseResponse()


def mock_sign_in(*args, **kwargs):
    return MockSupabaseResponse()


def mock_get_user(*args, **kwargs):
    return MockSupabaseResponse()


# Apply the mocks
AuthService.register_user = mock_sign_up
AuthService.authenticate_user = mock_sign_in
AuthService.get_current_user = mock_get_user


def test_register_endpoint(test_user_data):
    """Test user registration endpoint"""
    response = client.post(
        "/api/v1/auth/register",
        json=test_user_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert "password" not in data  # Ensure password is not returned
    assert data["role"] == test_user_data["role"]


def test_login_endpoint(test_user_data):
    """Test user login endpoint"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": test_user_data["email"],  # OAuth2 form expects username but we use email
            "password": test_user_data["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_logout_endpoint():
    """Test user logout endpoint"""
    # First login to get a token
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "testpassword123"
        }
    )
    token = login_response.json()["access_token"]
    
    # Then test logout with the token
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Logged out successfully"