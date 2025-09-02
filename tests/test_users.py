import pytest
from fastapi.testclient import TestClient
from BlogAPI.main import app

client = TestClient(app)

@pytest.mark.parametrize("user_id", [(1),(2),(3)])
def test_read_users(user_id):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200 or response.status_code == 404
    assert isinstance(response.json(), dict)
    if response.status_code == 200:
        assert response.json().get("id") == user_id
        
def test_create_delete_user():
    response = client.post("/users/", json={"name": "Test User", "email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    assert response.json().get("id") is not None
    
    #response = client.delete("/users/")
    #assert response.status_code == 204