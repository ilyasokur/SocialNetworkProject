import pytest
from unittest.mock import MagicMock
from app.service.auth import AuthService
from app.domain.models import User
from app.domain.schemas import UserCreate

@pytest.fixture
def mock_dao():
    mock = MagicMock()
    mock.get_user_by_username.return_value = None
    def mock_create_user(user):
        user.id = 1
        return user
    
    mock.create_user.side_effect = mock_create_user
    return mock

def test_register_user(mock_dao):
    auth_service = AuthService(mock_dao)

    user_data = UserCreate(username="testuser", email="test@mail.com", password="123456")
    user = auth_service.register_user(user_data)

    assert user.username == "testuser"
    assert user.email == "test@mail.com"
    assert mock_dao.create_user.called
