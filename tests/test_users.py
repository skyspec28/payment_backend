# tests/test_users.py
import pytest

from app.config import settings
from jose import jwt





def test_read_root(client,session):
    res = client.get("/")
    assert res.status_code == 200

def test_create_user(client,session):
    res = client.post("/user/", json={"email": "test@mail.com", "password": "12345"})
    assert res.status_code == 201
    assert res.json()["email"] == "test@mail.com"

def test_login_user(client,login_persist):
    res = client.post("/login", data={"username": "test@mail.com", "password": "12345"})
    token=jwt.decode(res.json()["access_token"], settings.secret_key, algorithms=settings.algorithm)
    assert token["user_id"] == 1
    print(res.json())
    assert res.status_code == 200



@pytest.mark.parametrize("email, password, status_code, detail", [
    ("test@mail.com", "wrongpassword", 403, "invalid credentials"),
    ("wrong@mail.com", "12345", 403, "invalid credentials"),
    ("notanemail", "12345", 403, "invalid credentials"),
    ("", "12345", 403, None),  # FastAPI validation error
    ("test@mail.com", "", 403, None),  # FastAPI validation error
])
def test_incorrect_login(client, login_persist, email, password, status_code, detail):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    if detail:
        assert res.json().get("detail") == detail
