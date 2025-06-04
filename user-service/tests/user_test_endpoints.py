import requests
from uuid import uuid4

BASE_URL = "http://localhost:8001/api/v1"

uuid_test = uuid4()

def test_register():
    url = f"{BASE_URL}/register"
    payload = {
        "email": f"testuser{uuid_test}@example.com",
        "username": f"testuser{uuid_test}",
        "hashed_password": "testpass"
    }

    response = requests.post(url, json=payload)
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == f"testuser{uuid_test}@example.com"
    assert "id" in data

def test_login():
    url = f"{BASE_URL}/login"
    payload = {
        "username": f"testuser{uuid_test}",
        "password": f"testpass"
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

def test_validate():
    login_url = f"{BASE_URL}/login"
    login_payload = {"username": f"testuser{uuid_test}", "password": "testpass"}
    login_resp = requests.post(login_url, json=login_payload)
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    headers = {"Authorization": f"{token}"}
    validate_url = f"{BASE_URL}/validate"
    validate_resp = requests.get(validate_url, headers=headers)
    print(validate_resp.json())
    assert validate_resp.status_code == 200
    data = validate_resp.json()
    assert data["username"] == f"testuser{uuid_test}"
