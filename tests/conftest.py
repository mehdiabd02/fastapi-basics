from app.routers import post
from app.schemas import Post
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_access_token
from app import models
import pytest

from app.database import Base, get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgresql@localhost:5432/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def test_user(client):
    user_data = {"email": "test@example.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    created_user = res.json()
    created_user["password"] = user_data["password"]
    return created_user

@pytest.fixture()
def token(client, test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client





@pytest.fixture()
def test_posts(test_user, session):
    posts_data = [
        {"title": "First Post", "content": "Content of the first post", "owner_id": test_user['id']},
        {"title": "Second Post", "content": "Content of the second post", "owner_id": test_user['id']}
    ]
    def create_posts_model(post):
        return models.Post(**post)

    post_map = map(create_posts_model, posts_data)
    session.add_all(post_map)
    session.commit()
    posts = session.query(models.Post).order_by(models.Post.id).all()
    return posts