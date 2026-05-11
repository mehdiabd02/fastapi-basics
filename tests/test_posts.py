from typing import List
from app import models, schemas
from app.oauth2 import create_access_token
from fastapi.testclient import TestClient
from app.main import app
import pytest

def test_get_all_posts(authorized_client, test_user, test_posts):
    response = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, response.json())
    posts_list = list(posts_map)

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(posts_list) == len(test_posts)
    
    # Verify all test posts are in the response
    response_ids = {post.Post.id for post in posts_list}
    test_ids = {post.id for post in test_posts}
    assert response_ids == test_ids
    
def test_unauthorized_access(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    post_id = test_posts[0].id
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 401

def test_get_one_post_does_not_exist(authorized_client):
    response = authorized_client.get("/posts/9999")
    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    post_id = test_posts[0].id
    response = authorized_client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    post = schemas.PostOut(**response.json())
    assert post.Post.id == post_id


@pytest.mark.parametrize("title, content", [
    ("New Post", "Content of the new post"),
    ("Another Post", "Content of another post")
])
def test_create_post(authorized_client, test_user, title, content):
    post_data = {"title": title, "content": content}
    response = authorized_client.post("/posts/", json=post_data)
    assert response.status_code == 201
    created_post = schemas.Post(**response.json())
    assert created_post.title == post_data["title"]
    assert created_post.content == post_data["content"]
    assert created_post.owner_id == test_user['id']

def test_create_post_unauthorized(client):
    post_data = {"title": "Unauthorized Post", "content": "This should not be created"}
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    post_id = test_posts[0].id
    response = client.delete(f"/posts/{post_id}")
    assert response.status_code == 401

def test_delete_post(authorized_client, test_posts):
    post_id = test_posts[0].id
    response = authorized_client.delete(f"/posts/{post_id}")
    assert response.status_code == 204

def test_delete_post_does_not_exist(authorized_client):
    response = authorized_client.delete("/posts/9999")
    assert response.status_code == 404

def test_delete_post_not_owner(client, authorized_client, test_posts):
    # Create a new user (unauthenticated client) and get a token for that user
    new_user_data = {"email": "newuser@example.com", "password": "password123"}
    new_user_response = client.post("/users/", json=new_user_data)
    assert new_user_response.status_code == 201
    new_user = schemas.UserOut(**new_user_response.json())

    # Authenticate as the new user using a separate TestClient instance
    token = create_access_token({"user_id": new_user.id})
    new_client = TestClient(app)
    new_client.headers = {**new_client.headers, "Authorization": f"Bearer {token}"}

    # Try to delete a post that doesn't belong to the new user
    post_id = test_posts[0].id
    response = new_client.delete(f"/posts/{post_id}")
    assert response.status_code == 403

def test_update_post(authorized_client, test_posts):
    post_id = test_posts[0].id
    update_data = {"title": "Updated Title", "content": "Updated Content"}
    response = authorized_client.put(f"/posts/{post_id}", json=update_data)
    assert response.status_code == 200
    updated_post = schemas.Post(**response.json())
    assert updated_post.title == update_data["title"]
    assert updated_post.content == update_data["content"]


def test_update_post_not_owner(client, authorized_client, test_posts):
    # Create a new user (unauthenticated client) and get a token for that user
    new_user_data = {"email": "newuser@example.com", "password": "password123"}
    new_user_response = client.post("/users/", json=new_user_data)
    assert new_user_response.status_code == 201
    new_user = schemas.UserOut(**new_user_response.json())

    # Authenticate as the new user using a separate TestClient instance
    token = create_access_token({"user_id": new_user.id})
    new_client = TestClient(app)
    new_client.headers = {**new_client.headers, "Authorization": f"Bearer {token}"}

    # Try to update a post that doesn't belong to the new user
    post_id = test_posts[0].id
    update_data = {"title": "Updated Title", "content": "Updated Content"}
    response = new_client.put(f"/posts/{post_id}", json=update_data)
    assert response.status_code == 403