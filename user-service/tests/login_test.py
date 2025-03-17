import pytest
from unittest.mock import MagicMock
from app.service.auth import AuthService
from app.domain.models import User
from app.domain.schemas import UserLogin
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def mock_dao():
    mock = MagicMock()
    user = User(username="testuser", hashed_password=pwd_context.hash("123456"))
    mock.get_user_by_username.return_value = user
    return mock

def test_authenticate_user(mock_dao):
    auth_service = AuthService(mock_dao)

    login_data = UserLogin(username="testuser", password="123456")
    token = auth_service.authenticate_user(login_data)

    assert "access_token" in token
    assert "token_type" in token

def test_authenticate_user_invalid(mock_dao):
    auth_service = AuthService(mock_dao)

    login_data = UserLogin(username="testuser", password="wrongpass")

    with pytest.raises(ValueError) as exc:
        auth_service.authenticate_user(login_data)
    assert str(exc.value) == "Invalid credentials"
