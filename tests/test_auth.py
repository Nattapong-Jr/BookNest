import pytest
from app import create_app
from models import db
from models.user import User
from dotenv import load_dotenv
import os

load_dotenv()  # โหลดค่าจาก .env

def test_login_success(app, client):
    with app.app_context():
        user = User(
            name="Tester",
            email="tester@example.com",
            password_hash="1234",
            role="user",
        )
        db.session.add(user)
        db.session.commit()
        user_id = user.id

    response = client.post(
        "/login",
        data={
            "email": "tester@example.com",
            "password": "1234",
        },
        follow_redirects=False,
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert session["user_id"] == user_id
        assert session["user_name"] == "Tester"
        assert session["user_role"] == "user"
        assert session["user_email"] == "tester@example.com"


def test_login_wrong_password(app, client):
    with app.app_context():
        user = User(
            name="Tester",
            email="tester@example.com",
            password_hash="1234",
            role="user",
        )
        db.session.add(user)
        db.session.commit()

    response = client.post(
        "/login",
        data={
            "email": "tester@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 200

    with client.session_transaction() as session:
        assert "user_id" not in session


def test_login_unknown_email(client):
    response = client.post(
        "/login",
        data={
            "email": "unknown@example.com",
            "password": "1234",
        },
    )

    assert response.status_code == 200

    with client.session_transaction() as session:
        assert "user_id" not in session

