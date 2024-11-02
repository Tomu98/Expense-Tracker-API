import pytest
from pydantic import ValidationError
from app.schemas.user import UserSignUp, UpdateAccount



def test_invalid_username_format_signup():
    """
    Ensure ValidationError for invalid characters in username.
    """
    with pytest.raises(ValidationError):
        UserSignUp(
            username="invalid username!",
            email="valid@example.com",
            password="securepassword",
            confirm_password="securepassword"
        )


def test_passwords_do_not_match_signup():
    """
    Ensure ValidationError when passwords don't match.
    """
    with pytest.raises(ValidationError):
        UserSignUp(
            username="valid_user",
            email="valid@example.com",
            password="securepassword",
            confirm_password="differentpassword"
        )


def test_invalid_username_format_update_account():
    """
    Ensure ValidationError for invalid characters in username on update.
    """
    with pytest.raises(ValidationError):
        UpdateAccount(username="invalid username!")


def test_valid_user_signup():
    """
    Verify UserSignUp instance creation with valid data.
    """
    user = UserSignUp(
        username="valid_user",
        email="valid@example.com",
        password="securepassword",
        confirm_password="securepassword"
    )
    assert user.username == "valid_user"
    assert user.email == "valid@example.com"


def test_username_length_limits_signup():
    """
    Ensure ValidationError for username outside length limits (3-30).
    """
    with pytest.raises(ValidationError):
        UserSignUp(username="ab", email="valid@example.com", password="securepassword", confirm_password="securepassword")
    
    with pytest.raises(ValidationError):
        UserSignUp(username="a" * 31, email="valid@example.com", password="securepassword", confirm_password="securepassword")


def test_password_length_limits_signup():
    """
    Ensure ValidationError for password below minimum length (8).
    """
    with pytest.raises(ValidationError):
        UserSignUp(username="valid_user", email="valid@example.com", password="short", confirm_password="short")
