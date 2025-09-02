import pytest
from BlogAPI import schemas
from jose import jwt
from BlogAPI.config import settings

@pytest.mark.parametrize("blog_id", [0, 1, 2])
def test_get_all_blogs(authorized_client, test_blogs, blog_id):
    response = authorized_client.get("/blogs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == len(test_blogs)
    assert response.json()[blog_id]["Blog"]["title"] == test_blogs[blog_id].title
    assert response.json()[blog_id]["Blog"]["body"] == test_blogs[blog_id].body
    assert response.json()[blog_id]["Blog"]["creator"]["id"] == test_blogs[blog_id].user_id