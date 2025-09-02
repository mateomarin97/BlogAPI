import pytest
from BlogAPI import schemas
from jose import jwt
from BlogAPI.config import settings

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

def test_login(client, test_user):
    #Notice we have /login not /login/ since we did not use prefixes when defining the route
    #Also notice we are using form data not json.
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    token = schemas.Token.model_validate(response.json())

    #Now we decode the token
    payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user_id=payload.get("id")
    
    assert username == test_user["email"]
    assert user_id == test_user["id"]
    assert token.token_type == "bearer"