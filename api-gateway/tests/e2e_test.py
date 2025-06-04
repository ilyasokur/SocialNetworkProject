import pytest
import requests
import time
from uuid import uuid4

BASE_URL = "http://localhost:8000"
TEST_USERNAME = f"test_user_{uuid4().hex[:8]}"
TEST_EMAIL = f"{TEST_USERNAME}@example.com"
TEST_PASSWORD = "testpass123"
auth_token = None
created_post_id = None
user_id = None

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown():
    global auth_token
    global user_id
    
    register_data = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
        "hashed_password": TEST_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/user/api/v1/register", json=register_data)
    assert response.status_code == 200
    user_id = response.json().get('id')
    
    login_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    response = requests.post(f"{BASE_URL}/user/api/v1/login", json=login_data)
    assert response.status_code == 200
    auth_token = response.json().get("access_token")
    
    assert auth_token is not None
    
    yield

def test_user_profile():
    headers = {"Authorization": f"{auth_token}"}
    print(headers)
    response = requests.get(f"{BASE_URL}/user/api/v1/validate", headers=headers)
    
    assert response.status_code == 200
    profile_data = response.json()
    print(profile_data)
    assert profile_data["username"] == TEST_USERNAME
    assert profile_data["email"] == TEST_EMAIL

def test_create_post():
    global created_post_id
    
    headers = {"Authorization": f"{auth_token}"}
    post_data = {
        "title": "Test Post",
        "description": "This is a test post",
        "is_private": False,
        "tags": ["test", "pytest"],
        "loyalty_platform": "test.com"
    }
    
    time.sleep(1)
    
    response = requests.post(
        f"{BASE_URL}/posts/create_post", 
        json=post_data, 
        headers=headers
    )
    print(response.json())
    
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data['post']
    created_post_id = response_data['post']["id"]

@pytest.mark.depends(on=['test_create_post'])
def test_get_post():
    headers = {"Authorization": f"{auth_token}"}
    post_data = {
        "id": created_post_id,
    }
    
    time.sleep(1)
    
    response = requests.post(
        f"{BASE_URL}/posts/get_post", 
        json=post_data, 
        headers=headers
    )
    
    assert response.status_code == 200
    post = response.json()
    assert post['post']["id"] == created_post_id
    assert post['post']["title"] == "Test Post"

@pytest.mark.depends(on=['test_create_post'])
def test_update_post():
    headers = {"Authorization": f"{auth_token}"}
    update_data = {
        "id": created_post_id,
        "title": "Updated Test Post",
        "description": "This is an updated test post",
        "is_private": True,
        "tags": ["updated", "test"],
        "loyalty_platform": "updated.com"
    }
    
    time.sleep(1)
    
    response = requests.put(
        f"{BASE_URL}/posts/update_post", 
        json=update_data, 
        headers=headers
    )
    
    assert response.status_code == 200
    
    get_response = requests.post(
        f"{BASE_URL}/posts/get_post", 
        json={"id": created_post_id, "user_id": user_id}, 
        headers=headers
    )
    updated_post = get_response.json()
    print(updated_post)
    assert updated_post['post']["title"] == "Updated Test Post"
    assert updated_post['post']["isPrivate"] is True

def test_add_comment():
    headers = {"Authorization": f"{auth_token}"}
    comment_data = {
        "post_id": created_post_id,
        "content": "Test comment from pytest"
    }
    
    time.sleep(1)
    
    response = requests.post(
        f"{BASE_URL}/posts/add_comment", 
        json=comment_data, 
        headers=headers
    )
    
    assert response.status_code == 200

def test_like_post():
    headers = {"Authorization": f"{auth_token}"}
    like_data = {
        "post_id": created_post_id
    }
    
    time.sleep(1)
    
    response = requests.post(
        f"{BASE_URL}/posts/like_post", 
        json=like_data, 
        headers=headers
    )
    
    assert response.status_code == 200

@pytest.mark.depends(on=['test_create_post', 'test_update_post'])
def test_delete_post():
    headers = {"Authorization": f"{auth_token}"}
    delete_data = {
        "id": created_post_id,
    }
    
    time.sleep(1)
    
    response = requests.delete(
        f"{BASE_URL}/posts/delete_post", 
        json=delete_data, 
        headers=headers
    )
    print(response.json())
    assert response.status_code == 200
    
    get_response = requests.post(
        f"{BASE_URL}/posts/get_post", 
        json=delete_data, 
        headers=headers
    )
    assert get_response.status_code == 500

def test_get_post_stats():
    headers = {"Authorization": f"{auth_token}"}
    stats_data = {
        "post_id": created_post_id
    }
    
    time.sleep(1)
    
    response = requests.post(
        "http://localhost:8000/statistics/get_post_stats", 
        json=stats_data, 
        headers=headers
    )
    print(response.json())
    assert response.status_code == 200
    stats = response.json()
    assert "views" in stats
    assert "likes" in stats
    assert "comments" in stats

def test_get_post_view_dynamics():
    headers = {"Authorization": f"{auth_token}"}
    dynamics_data = {
        "post_id": created_post_id,
        "from_date": "2023-01-01",
        "to_date": "2025-10-10"
    }
    
    time.sleep(1)
    
    response = requests.post(
        f"{BASE_URL}/statistics/get_post_view_dynamics", 
        json=dynamics_data,
        headers=headers
    )
    print(response.json())
    
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_get_top_posts():
    headers = {"Authorization": f"{auth_token}"}
    top_data = {
        "stat_type": "likes",
        "limit": 3
    }
    
    time.sleep(1)
    
    response = requests.post(
        f"{BASE_URL}/statistics/get_top_posts", 
        json=top_data, 
        headers=headers
    )
    
    assert response.status_code == 200
    top_posts = response.json()
    assert isinstance(top_posts, dict)
    assert len(top_posts) <= 3