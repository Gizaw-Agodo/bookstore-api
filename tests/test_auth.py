import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.models.user import User
from app.core.security import create_url_safe_token, hash_password
from app.core.config import settings
from uuid import UUID

class TestAuthRoutes:
    @pytest.mark.asyncio
    async def test_create_user(self, client: TestClient, mock_auth_service: MagicMock, mock_email_service: MagicMock):
        """Test user creation with mocking."""
        
        # Configure the mock to return a mock object with attributes
        # that behave like a real User model instance.
        mock_user = MagicMock(spec=User)
        mock_user.id = UUID("123e4567-e89b-12d3-a456-426614174000")
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        mock_auth_service.create_user.return_value = mock_user

        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = client.post("/api/v1/auth/signup", json=user_data)
        
        assert response.status_code == 201
        
        # Check that the email service was called correctly with the mocked user data
        mock_email_service.send_email.assert_called_once()
        call_args = mock_email_service.send_email.call_args[1]
        assert call_args['recipients'] == [mock_user.email]
        assert call_args['template_body']['username'] == mock_user.username

    @pytest.mark.asyncio
    async def test_create_user_with_existing_email(self, client: TestClient, mock_user_service: MagicMock):
        """Test user creation with an existing email, with a mock user object."""
        
        # Configure the mock to return a mock object that behaves like an existing user
        mock_existing_user = MagicMock(spec=User)
        mock_existing_user.email = "existing@example.com"
        mock_user_service.get_user_by_email.return_value = mock_existing_user
        
        user_data = {
            "username": "auser",
            "email": "existing@example.com",
            "password": "newpassword",
            "first_name": "Another",
            "last_name": "User"
        }
        
        response = client.post("/api/v1/auth/signup", json=user_data)
        
        assert response.status_code == 400
        assert response.json()["detail"] == "User With The Email Exists"

    @pytest.mark.asyncio
    async def test_verify_email_token(self, client: TestClient, mock_user_service: MagicMock):
        """Test verifying an email token."""
        # Create a valid token
        token_data = {"email": "test@example.com"}
        token = create_url_safe_token(token_data)

        # Mock the verify_user method to return a user
        mock_user = MagicMock(spec=User)
        mock_user.email = "test@example.com"
        mock_user_service.verify_user.return_value = mock_user
        
        response = client.post(f"/api/v1/auth/verify/{token}")
        
        assert response.status_code == 200
        mock_user_service.verify_user.assert_called_once_with(token_data['email'], MagicMock())
        assert response.json()["message"] == "email verified successfuly"
        
    @pytest.mark.asyncio
    async def test_user_login_success(self, client: TestClient, mock_auth_service: MagicMock):
        """Test a successful user login."""
        
        mock_user = MagicMock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.id = UUID("123e4567-e89b-12d3-a456-426614174000")
        mock_user.username = "testuser"
        
        mock_auth_service.login.return_value = {
            "user": mock_user,
            "access_token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
        }
        
        login_data = {"email": "test@example.com", "password": "password123"}
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["message"] == "Login successfull"
        assert "access_token" in response_json
        assert "refresh_token" in response_json
        assert response_json["user"]["email"] == "test@example.com"
        
    @pytest.mark.asyncio
    async def test_user_login_failure(self, client: TestClient, mock_auth_service: MagicMock):
        """Test user login with incorrect credentials."""
        
        from app.core.errors import Unauthorized
        
        mock_auth_service.login.side_effect = Unauthorized("Invalid credentials provided")
        
        login_data = {"email": "test@example.com", "password": "wrongpassword"}
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials provided"
        
    @pytest.mark.asyncio
    async def test_forgot_password(self, client: TestClient, mock_user_service: MagicMock, mock_email_service: MagicMock):
        """Test the forgot password endpoint."""
        
        mock_user = MagicMock(spec=User)
        mock_user.username = "testuser"
        mock_user.email = "test@example.com"
        mock_user_service.get_user_by_email.return_value = mock_user

        forgot_password_data = {"email": "test@example.com"}
        response = client.post("/api/v1/auth/forgot-password", json=forgot_password_data)
        
        assert response.status_code == 200
        assert response.json()["Message"] == "Password reset email sent successfully"
        mock_email_service.send_email.assert_called_once()
        call_args = mock_email_service.send_email.call_args[1]
        assert call_args['recipients'] == [forgot_password_data['email']]
        assert 'reset_link' in call_args['template_body']

    @pytest.mark.asyncio
    async def test_reset_password(self, client: TestClient, mock_auth_service: MagicMock):
        """Test the reset password endpoint."""
        
        mock_auth_service.reset_password.return_value = None
        
        # Create a valid token
        token_data = {"email": "test@example.com"}
        token = create_url_safe_token(token_data)

        reset_data = {"new_password": "newpassword123", "confirm_password": "newpassword123"}
        response = client.post(f"/api/v1/auth/reset-password/{token}", json=reset_data)
        
        assert response.status_code == 200
        assert response.json()["message"] == "password reseted successfuly"
        mock_auth_service.reset_password.assert_called_once()