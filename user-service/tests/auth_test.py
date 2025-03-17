import jwt
import pytest
from unittest.mock import patch
from fastapi import HTTPException
from app.api.routes import verify_token

KEYCLOAK_MOCK_CERTS = {
    "keys": [
        {
            "kid": "test-key",
            "kty": "RSA",
            "alg": "RS256",
            "use": "sig",
            "n": "test-n",
            "e": "test-e",
            "x5c": ["test-cert"]
        }
    ]
}

@pytest.fixture
def fake_jwt_hs256():
    return jwt.encode({"sub": "testuser"}, "your_hs256_secret", algorithm="HS256")

@pytest.fixture
def fake_jwt_rs256():
    return jwt.encode({"sub": "testuser"}, "test-public-key", algorithm="RS256", headers={"kid": "test-key"})

def test_verify_token_invalid():
    with pytest.raises(HTTPException) as exc:
        verify_token("invalid.token")
    assert exc.value.status_code == 401
