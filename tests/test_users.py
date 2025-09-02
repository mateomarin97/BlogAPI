import pytest
from BlogAPI import schemas
from BlogAPI.tests.database import client, session

@pytest.mark.parametrize("user_id", [(1),(2),(3)])
def test_read_users(user_id, client):
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200 or response.status_code == 404
    assert isinstance(response.json(), dict)
    if response.status_code == 200:
        assert response.json().get("id") == user_id
        
def test_create_user(client):
    response = client.post("/users/", json={"name": "Test User", "email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 201
    assert isinstance(response.json(), dict)
    new_user = schemas.ShowUser.model_validate(response.json()) 
    assert new_user.id is not None
    