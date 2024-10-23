from fastapi import status
from app.schemas.user import UserSignUp


def test_signup_succes(client):
    user_data = UserSignUp(
        username="testuser",
        email="test@example.com",
        password="testpassword",
        confirm_password="testpassword"
    ).model_dump()

    response = client.post("/signup", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert "detail" in response_data
    assert "id" in response_data
    assert response_data["detail"] == f"User '{user_data['username']}' successfully registered"


def test_signup_email_exists(client):
    pass


def test_signup_username_taken(client):
    pass
