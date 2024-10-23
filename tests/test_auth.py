from fastapi import status
from app.models.user import User
from app.schemas.user import UserSignUp



def create_user_for_test(client, username, email, password):
    """
    Create a user for testing purposes.

    Args:
        client: Test client for API requests.
        username: The username for the new user.
        email: The email for the new user.
        password: The password for the new user.

    Returns:
        The response from the signup endpoint.
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
        client: Test client for API requests.
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
        client: Test client for API requests.
        db: Database session for verifying user existence.
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
        client: Test client for API requests.
        db: Database session for verifying user existence.
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
