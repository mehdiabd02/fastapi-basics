from jose import jwt
import pytest
from app import schemas
from app.config import settings


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!!!"}


def test_create_user(client):
    response = client.post("/users/", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 201
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "test@example.com"


def test_user_login(client, test_user):
    response = client.post("/login/", data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200
    token = schemas.Token(**response.json())
    payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    assert payload.get("user_id") is not None
    assert token.access_token is not None


@pytest.mark.parametrize("email, password, expected_status", [
    ("test@example.com", "wrongpassword", 403),
    (None, "password123", 422)
])
def test_incorrect_login(client, test_user, email, password, expected_status):
    response = client.post("/login/", data={"username": email, "password": password})
    assert response.status_code == expected_status

