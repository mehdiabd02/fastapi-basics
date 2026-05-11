from app.database import SessionLocal, get_db
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import Base
import pytest
from alembic import command
from alembic.config import Config



SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgresql@localhost:5432/test_db'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)  # Create tables for testing

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)  # Drop all tables before each test
    Base.metadata.create_all(bind=engine)  # Create tables for testing
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@pytest.fixture()
def client(session):
    with TestClient(app) as c:
        yield c