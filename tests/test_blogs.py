import pytest

@pytest.mark.parametrize("blog_id", [0, 1, 2])
def test_get_all_blogs(authorized_client, test_blogs, blog_id):
    response = authorized_client.get("/blogs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == len(test_blogs)
    assert response.json()[blog_id]["Blog"]["title"] == test_blogs[blog_id].title
    assert response.json()[blog_id]["Blog"]["body"] == test_blogs[blog_id].body
    assert response.json()[blog_id]["Blog"]["creator"]["id"] == test_blogs[blog_id].user_id
    
def test_unauthorized_user_get_all_blogs(client):
    response = client.get("/blogs/")
    assert response.status_code == 401
    
def test_unauthorized_user_get_one_blog(client, test_blogs):
    response = client.get(f"/blogs/{test_blogs[0].id}")
    assert response.status_code == 401

def test_get_one_non_existing_blog(authorized_client):
    response = authorized_client.get("/blogs/999")
    assert response.status_code == 404
    
def test_get_one_blog(authorized_client, test_blogs):
    response = authorized_client.get(f"/blogs/{test_blogs[0].id}")
    assert response.status_code == 200
    assert response.json()["Blog"]["title"] == test_blogs[0].title
    assert response.json()["Blog"]["body"] == test_blogs[0].body
    assert response.json()["Blog"]["creator"]["id"] == test_blogs[0].user_id
    
def test_create_blog(authorized_client, test_user):
    response = authorized_client.post("/blogs/", json={
        "title": "New Blog",
        "body": "This is the body of the new blog"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "New Blog"
    assert response.json()["body"] == "This is the body of the new blog"
    assert response.json()["user_id"] == test_user["id"]
    assert response.json()["published"] is True

def test_unauthorized_create_blog(client):
    response = client.post("/blogs/", json={
        "title": "New Blog",
        "body": "This is the body of the new blog"
    })
    assert response.status_code == 401
    
def test_unauthorized_delete_blog(client, test_blogs):
    response = client.delete(f"/blogs/{test_blogs[0].id}")
    assert response.status_code == 401
    
def test_delete_blog(authorized_client, test_blogs):
    response = authorized_client.delete(f"/blogs/{test_blogs[0].id}")
    assert response.status_code == 204
    
def test_delete_non_existing_blog(authorized_client):
    response = authorized_client.delete("/blogs/999")
    assert response.status_code == 404

def test_delete_other_user_blog(authorized_client, test_blogs_other_user):
    response = authorized_client.delete(f"/blogs/{test_blogs_other_user[0].id}")
    assert response.status_code == 403
    
def test_update_blog(authorized_client, test_blogs):
    response = authorized_client.put(f"/blogs/{test_blogs[0].id}", json={
        "title": "Updated Blog",
        "body": "This is the updated body of the blog"
    })
    assert response.status_code == 202
    response = authorized_client.get(f"/blogs/{test_blogs[0].id}")
    assert response.json()["Blog"]["title"] == "Updated Blog"
    assert response.json()["Blog"]["body"] == "This is the updated body of the blog"
    assert response.json()["Blog"]["creator"]["id"] == test_blogs[0].user_id

def test_update_other_user_blog(authorized_client, test_blogs_other_user):
    response = authorized_client.put(f"/blogs/{test_blogs_other_user[0].id}", json={
        "title": "Updated Blog",
        "body": "This is the updated body of the blog"
    })
    assert response.status_code == 403
    
def test_unauthorized_update_blog(client, test_blogs):
    response = client.put(f"/blogs/{test_blogs[0].id}", json={
        "title": "Updated Blog",
        "body": "This is the updated body of the blog"
    })
    assert response.status_code == 401

def test_update_non_existing_blog(authorized_client):
    response = authorized_client.put("/blogs/999", json={
        "title": "Updated Blog",
        "body": "This is the updated body of the blog"
    })
    assert response.status_code == 404