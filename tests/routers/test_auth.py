from fastapi import status
from tests.utils import create_user_for_test



# Test for /signup endpoint
def test_signup_success(client):
    """
    Test successful user signup.
    """
    response = create_user_for_test(client, "testuser", "test@example.com", "testpasdword")
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert "detail" in response_data
    assert "id" in response_data
    assert response_data["detail"] == f"User 'testuser' successfully registered"


def test_signup_email_exists(client):
    """
    Test handling of duplicate email during signup.
    """
    create_user_for_test(client, "testuser1", "duplicate@example.com", "testpassword")

    response = create_user_for_test(client, "testuser2", "duplicate@example.com", "testpassword2")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Email already registered."


def test_signup_username_taken(client):
    """
    Test handling of duplicate username during signup.
    """
    create_user_for_test(client, "duplicateuser", "test@example.com", "testpassword")

    response = create_user_for_test(client, "duplicateuser", "test2@example.com", "testpassword")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Username already taken."



# Tests for /login endpoint
def test_login_success(client):
    """
    Test successful login of a user.
    """
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_login(client):
    """
    Test login with invalid credentials.
    """
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    invalid_username_data = {"username": "wronguser", "password": "testpassword"}
    invalid_password_data = {"username": "testuser", "password": "wrongpassword"}

    response1 = client.post("/login", data=invalid_username_data)
    response2 = client.post("/login", data=invalid_password_data)

    assert response1.status_code == status.HTTP_401_UNAUTHORIZED
    assert response2.status_code == status.HTTP_401_UNAUTHORIZED
    assert response1.json()["detail"] == "Invalid credentials."
    assert response2.json()["detail"] == "Invalid credentials."


def test_missing_login_fields(client):
    """
    Test login with missing credentials.
    """
    # No username or password provided
    missing_login_data = {}
    response = client.post("/login", data=missing_login_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Username provided but missing password
    incomplete_login_data = {"username": "testuser"}
    response = client.post("/login", data=incomplete_login_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_token_format(client):
    """
    Test the format of the JWT token returned after login.
    """
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    # Attempt to log in and get the token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK

    # Check that the token has the correct format (header.payload.signature)
    token = response.json().get("access_token")
    assert token is not None
    assert len(token.split(".")) == 3
