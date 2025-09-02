def test_upvote_blog(authorized_client, test_blogs):
    response = authorized_client.post(f"/vote/", json={"blog_id": test_blogs[0].id, "direction": 1})
    assert response.status_code == 201
    assert response.json()["message"] == "Vote created successfully"
    
def test_downvote_blog(authorized_client, test_blogs):
    blog_id = test_blogs[0].id
    response = authorized_client.post(f"/vote/", json={"blog_id": blog_id, "direction": 1})
    response = authorized_client.post(f"/vote/", json={"blog_id": blog_id, "direction": 0})
    assert response.status_code == 201
    assert response.json()["message"] == "Vote deleted successfully"
    
def test_double_upvote(authorized_client, test_blogs):
    blog_id = test_blogs[0].id
    response = authorized_client.post(f"/vote/", json={"blog_id": blog_id, "direction": 1})
    assert response.status_code == 201
    assert response.json()["message"] == "Vote created successfully"
    response = authorized_client.post(f"/vote/", json={"blog_id": blog_id, "direction": 1})
    assert response.status_code == 400
    assert response.json()["detail"] == "Vote already exists"
    
def test_downvote_without_upvote(authorized_client, test_blogs):
    blog_id = test_blogs[0].id
    response = authorized_client.post(f"/vote/", json={"blog_id": blog_id, "direction": 0})
    assert response.status_code == 404
    assert response.json()["detail"] == "Vote not found"
    
def test_unathorized_vote(client, test_blogs):
    blog_id = test_blogs[0].id
    response = client.post(f"/vote/", json={"blog_id": blog_id, "direction": 1})
    assert response.status_code == 401
