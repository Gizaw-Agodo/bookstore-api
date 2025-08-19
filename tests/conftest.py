import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.core.dependencies import (get_session, get_user_service,
                     get_auth_service, get_email_service)

from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.email_service import EmailService


@pytest.fixture
def mock_session() -> MagicMock:
    return MagicMock()

@pytest.fixture
def mock_user_service() -> MagicMock:
    return MagicMock(spec=UserService)

@pytest.fixture
def mock_auth_service(mock_user_service: MagicMock) -> MagicMock:
    service = MagicMock(spec=AuthService)
    service.user_service = mock_user_service
    return service
    
@pytest.fixture
def mock_email_service() -> MagicMock:
    return MagicMock(spec=EmailService)

@pytest.fixture
def client(
    mock_session: MagicMock, 
    mock_user_service: MagicMock, 
    mock_auth_service: MagicMock,
    mock_email_service: MagicMock
) :
    def override_get_session():
        yield mock_session

    def override_get_user_service():
        return mock_user_service

    def override_get_auth_service():
        return mock_auth_service
    
    def override_get_email_service():
        return mock_email_service
        
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_user_service] = override_get_user_service
    app.dependency_overrides[get_auth_service] = override_get_auth_service
    app.dependency_overrides[get_email_service] = override_get_email_service

    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()