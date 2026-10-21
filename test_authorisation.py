
from unittest.mock import patch

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@patch("src.routes.auth.authorise_user")
def test_login_success(mock_authorise):
    mock_authorise.return_value = "fake.jwt.token"

    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "token": "fake.jwt.token"
    }

    mock_authorise.assert_called_once()


@patch("src.routes.auth.authorise_user")
def test_login_invalid_credentials(mock_authorise):
    mock_authorise.return_value = None

    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password"
    }


@patch("src.routes.auth.authorise_user")
def test_login_missing_password(mock_authorise):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "test@example.com"
        }
    )

    assert response.status_code == 400

    mock_authorise.assert_not_called()


@patch("src.routes.auth.authorise_user")
def test_login_missing_email(mock_authorise):
    response = client.post(
        "/api/auth/login",
        json={
            "password": "password123"
        }
    )

    assert response.status_code == 400

    mock_authorise.assert_not_called()

