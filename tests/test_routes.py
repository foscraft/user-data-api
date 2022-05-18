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
    data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "bio": fake.text(),
        "password": fake.password(),
    }

    response = client.post(
        "/register", data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == 201
    assert response.json["message"] == "User created"


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
        "/register", data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == 201
    assert response.json["message"] == "User created"

    data = {
        "username": data["username"],
        "password": data["password"],
    }

    response = client.post(
        "/login", data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json["message"] == "User logged in"