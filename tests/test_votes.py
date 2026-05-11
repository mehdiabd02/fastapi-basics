import pytest
from app import schemas,models
from app.oauth2 import create_access_token

@pytest.fixture()
def test_votes(test_posts, test_user, session):
    vote_data = [
        {"post_id": test_posts[0].id, "user_id": test_user['id']},
        {"post_id": test_posts[1].id, "user_id": test_user['id']}
    ]
    votes = [models.Vote(**data) for data in vote_data]
    session.add_all(votes)
    session.commit()
    return votes
    assert response.status_code == 201

def test_vote_twice(authorized_client, test_posts):
    vote_data = {"post_id": test_posts[0].id, "dir": 1}
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 201
    # Try voting again on the same post
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 409

def test_delete_vote(authorized_client, test_posts):
    vote_data = {"post_id": test_posts[0].id, "dir": 1}
    # First, create a vote
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 201
    # Now, delete the vote
    vote_data["dir"] = 0
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 201