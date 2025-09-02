import pytest
from BlogAPI import schemas
from jose import jwt
from BlogAPI.config import settings

def test_get_all_blogs(authorized_client):
    response = authorized_client.get("/blogs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)