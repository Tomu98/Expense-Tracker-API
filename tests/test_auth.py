from fastapi import status
from app.models.user import User
from app.schemas.user import UserSignUp



def create_user_for_test(client, username, email, password):
    """
    Create a user for testing purposes.

    Args:
        client (TestClient): Test client for API requests.
        username (str): The username for the new user.
        email (EmailStr): The email for the new user.
        password (str): The password for the new user.

    Returns:
        response: The response from the signup endpoint.
    """
    user_data = UserSignUp(
        username=username,
        email=email,
        password=password,
        confirm_password=password
    ).model_dump()  # Serialize user data

    return client.post("/signup", json=user_data)



def test_signup_succes(client):
    """
    Test successful user signup.

    Args:
        client (TestClient):  The test client used to make HTTP requests.
    """
    response = create_user_for_test(client, "testuser", "test@example.com", "testpasdword")
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()
    assert "detail" in response_data
    assert "id" in response_data
    assert response_data["detail"] == f"User 'testuser' successfully registered"


def test_signup_email_exists(client, db):
    """
    Test handling of duplicate email during signup.

    Args:
        client (TestClient): The test client used to make HTTP requests.
        db (Session): Database session for verifying user existence.
    """
    response1 = create_user_for_test(client, "testuser", "duplicate@example.com", "testpassword")
    assert response1.status_code == status.HTTP_201_CREATED  # First signup should succeed

    # Check if user is created in the database
    user_in_db = db.query(User).filter(User.email == "duplicate@example.com").first()
    assert user_in_db is not None

    response2 = create_user_for_test(client, "testuser2", "duplicate@example.com", "testpassword2")
    assert response2.status_code == status.HTTP_400_BAD_REQUEST  # Second signup should fail

    response_data = response2.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Email already registered."


def test_signup_username_taken(client, db):
    """
    Test handling of duplicate username during signup.

    Args:
        client (TestClient): The test client used to make HTTP requests.
        db (Session): Database session for verifying user existence.
    """
    response1 = create_user_for_test(client, "duplicateuser", "test@example.com", "testpassword")
    assert response1.status_code == status.HTTP_201_CREATED  # First signup should succeed

    # Check if user is created in the database
    user_in_db = db.query(User).filter(User.username == "duplicateuser").first()
    assert user_in_db is not None

    response2 = create_user_for_test(client, "duplicateuser", "test2@example.com", "testpassword")
    assert response2.status_code == status.HTTP_400_BAD_REQUEST  # Second signup should fail

    response_data = response2.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Username already taken."



def test_login_succes(client):
    """
    Test successful login of a user.

    Ensures that a valid user can log in with correct credentials 
    and receive a valid JWT access token in response.

    Args:
        client (TestClient): The test client used to make HTTP requests.
    """
    response = create_user_for_test(client, "testuser", "test@example.com", "testpassword")
    assert response.status_code == status.HTTP_201_CREATED

    # Attempt to log in with correct credentials
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_login(client):
    """
    Test login with invalid credentials.

    Verifies that login fails and returns 401 Unauthorized 
    when provided with an incorrect username or password.

    Args:
        client (TestClient): The test client used to make HTTP requests.
    """
    response = create_user_for_test(client, "testuser", "test@example.com", "testpassword")
    assert response.status_code == status.HTTP_201_CREATED

    # Login with an incorrect username
    invalid_username_data = {"username": "wronguser", "password": "testpassword"}
    response = client.post("/login", data=invalid_username_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials."

    # Login with incorrect password
    invalid_password_data = {"username": "testuser", "password": "wrongpassword"}
    response = client.post("/login", data=invalid_password_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid credentials."


def test_missing_login_fields(client):
    """
    Test login with missing credentials.

    Verifies that login fails with 422 Unprocessable Entity when 
    the username or password is not provided in the request.

    Args:
        client (TestClient): The test client used to make HTTP requests.
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

    Verifies that the token has the expected structure (three parts separated by dots).

    Args:
        client (TestClient): The test client used to make HTTP requests.
    """
    response = create_user_for_test(client, "testuser", "test@example.com", "testpassword")
    assert response.status_code == status.HTTP_201_CREATED

    # Attempt to log in and get the token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)

    # Check that the token has the correct format (header.payload.signature)
    token = response.json().get("access_token")
    assert len(token.split(".")) == 3
