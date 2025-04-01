import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# tests/database.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from app.database import get_db
from app.config import settings
from app.oauth2 import create_access_token
from app import models

# Database URL for testing
SQLALCHEMY_DATABASE_URL = (
    f'postgresql://{settings.database_username}:{settings.database_password}'
    f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
)

# Create SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session Factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)



@pytest.fixture()
def login_persist(client):
    res = client.post("/user/", json={"email": "test@mail.com", "password": "12345"})
    assert res.status_code == 201
    new_user=res.json()
    
    return new_user




@pytest.fixture()
def token(login_persist):
    return create_access_token(data={"user_id":login_persist["id"]})

@pytest.fixture()
def auhtorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture()
def populated_post(login_persist, session):
    posts_data = [
        {
            "title": "First Test Post",
            "content": "This is the first test post content",
            "owner_id": login_persist["id"],
            "published": True,
            "created_at": "2024-01-01T00:00:00"
        },
        {
            "title": "Second Test Post",
            "content": "This is the second test post content",
            "owner_id": login_persist["id"],
            "published": True,
            "created_at": "2024-01-02T00:00:00"
        },
        {
            "title": "Third Test Post",
            "content": "This is the third test post content",
            "owner_id": login_persist["id"],
            "published": False,
            "created_at": "2024-01-03T00:00:00"
        }
    ]

    # def create_post_model(post):
    #     return models.Post(**post)

    # posts = list(map(create_post_model, posts_data))
    # session.add_all(posts)
    # session.commit()
    
    # return session.query(models.Post).all()
