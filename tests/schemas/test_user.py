import pytest
from pydantic import ValidationError
from app.schemas.user import UserSignUp, UpdateAccount



# Tests for UserSignUp
def test_invalid_username_format_signup():
    """
    Raise ValidationError for invalid characters in UserSignUp username.
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
    Raise ValidationError when passwords don't match in UserSignUp.
    """
    with pytest.raises(ValidationError):
        UserSignUp(
            username="valid_user",
            email="valid@example.com",
            password="securepassword",
            confirm_password="differentpassword"
        )


@pytest.mark.parametrize("username", ["ab", "a" * 31])
def test_username_length_limits_signup(username):
    """
    Raise ValidationError for username outside length limits in UserSignUp.
    """
    with pytest.raises(ValidationError):
        UserSignUp(username=username, email="valid@example.com", password="securepassword", confirm_password="securepassword")


def test_password_length_limits_signup():
    """
    Raise ValidationError for password below minimum length in UserSignUp.
    """
    with pytest.raises(ValidationError):
        UserSignUp(username="valid_user", email="valid@example.com", password="short", confirm_password="short")


def test_valid_user_signup():
    """
    Allow UserSignUp creation with valid data.
    """
    user = UserSignUp(
        username="valid_user",
        email="valid@example.com",
        password="securepassword",
        confirm_password="securepassword"
    )
    assert user.username == "valid_user"
    assert user.email == "valid@example.com"


# Tests for UpdateAccount
def test_invalid_username_format_update_account():
    """
    Raise ValidationError for invalid characters in UpdateAccount username.
    """
    with pytest.raises(ValidationError):
        UpdateAccount(username="invalid username!")
