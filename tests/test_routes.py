import json

import pytest
from faker import Faker

from app import app as myapp
from app.models import db

fake = Faker()


@pytest.fixture(scope="module")
def app():
    myapp.config.from_object("config.TestingConfig")  # other setup can go here
    with myapp.app_context():
        db.create_all()

    yield myapp


@pytest.fixture()
def client(app):
    yield app.test_client()


def test_register(client):
    test_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "bio": fake.text(),
        "password": fake.password(),
    }

    response = client.post(
        "/api/v1/register",
        data=json.dumps(test_data),
        content_type="application/json",
    )
    data = response.json.get("user")
    assert response.status_code == 201
    assert data.get("email") == test_data.get("email")
    assert data.get("username") == test_data.get("username")


def test_login(client):
    data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "bio": fake.text(),
        "password": fake.password(),
    }

    response = client.post(
        "/api/v1/register",
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 201

    response = client.post(
        "/api/v1/login",
        data=json.dumps(
            {
                "email": data["email"],
                "password": data["password"],
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert (
        response.json["message"] == f"You are logged in as {data['username']}"
    )


def test_update_user_by_id(client):
    data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "bio": fake.text(),
        "password": fake.password(),
    }

    response = client.post(
        "/api/v1/register",
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 201
    user_id = response.json["user"]["id"]

    updated_data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "bio": fake.text(),
    }

    response = client.put(
        f"/api/v1/users/{user_id}",
        data=json.dumps(updated_data),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json["message"] == "User updated"


def test_get_users(client):
    response = client.get("/api/v1/users")

    users = response.json["users"]
    assert response.status_code == 200
    assert type(users) == list


def test_get_user_by_id(client):
    data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "bio": fake.text(),
        "password": fake.password(),
    }

    response = client.post(
        "/api/v1/register",
        data=json.dumps(data),
        content_type="application/json",
    )
    user_id = response.json["user"]["id"]

    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 200
    assert type(response.json) == dict


def test_get_user_by_id_not_found(client):
    response = client.get("/api/v1/users/100")

    assert response.status_code == 404
