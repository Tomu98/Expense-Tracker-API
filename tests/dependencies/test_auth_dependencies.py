import pytest
from fastapi import HTTPException
from app.dependencies.auth import hash_password, authenticate_user, get_current_user
from app.dependencies.jwt import create_jwt
from tests.utils import create_user_for_test



def test_password_is_hashed():
    """
    Confirm that 'hash_password' returns a unique and secure hash.
    """
    password = "testpassword"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$2b$")  # Verify compliance with 'bcrypt' format



def test_authenticate_user_valid_credentials(client, db):
    """
    Authenticate correctly with valid credentials.
    """
    create_user_for_test(client, username="testuser", email="test@example.com", password="testpassword")

    user = authenticate_user("testuser", "testpassword", db)
    assert user is not False
    assert user.username == "testuser"


def test_authenticate_user_invalid_password(client, db):
    """
    Authentication fails with incorrect password.
    """
    create_user_for_test(client, username="testuser", email="test@example.com", password="testpassword")

    user = authenticate_user("testuser", "wrongpassword", db)
    assert user is False


def test_authenticate_user_nonexistent_user(db):
    """
    Authentication fails with non-existent user.
    """
    user = authenticate_user("nonexistent", "password123", db)
    assert user is False



def test_get_current_user_valid_token(client, db):
    """
    Retrieves the current user with a valid token.
    """
    response = create_user_for_test(client, username="testuser", email="test@example.com", password="testpassword")
    user_id = response.json()["id"]
    token = create_jwt({"id": user_id, "sub": "testuser"})

    user = get_current_user(token=token, db=db)
    assert user.username == "testuser"


def test_get_current_user_invalid_token(db):
    """
    Throws error with invalid token.
    """
    invalid_token = "invalid.token.string"

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=invalid_token, db=db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"


def test_get_current_user_user_not_found(db):
    """
    Throws error with non-existent user in the token.
    """
    non_existent_user_id = 9999
    token = create_jwt({"id": non_existent_user_id, "sub": "nonexistent"})

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token=token, db=db)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "User not found."
