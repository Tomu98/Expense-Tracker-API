import pytest
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException
from app.dependencies.jwt import create_jwt, decode_jwt, SECRET_KEY, ALGORITHM



@pytest.fixture
def test_data():
    return {"user_id": 123, "username": "testuser"}


def test_create_jwt_token_structure(test_data):
    """
    Ensure 'create_jwt' produces a valid token structure with the expected data.
    """
    token = create_jwt(test_data)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_token["user_id"] == test_data["user_id"]
    assert decoded_token["username"] == test_data["username"]
    assert "exp" in decoded_token


def test_create_jwt_custom_expiration(test_data):
    """
    Verify 'create_jwt' respects custom expiration times.
    """
    custom_exp = timedelta(minutes=1)
    token = create_jwt(test_data, expires_delta=custom_exp)
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    # Check that expiration is roughly 1 minute ahead of current time
    assert decoded_token["exp"] - decoded_token["iat"] <= custom_exp.total_seconds()


def test_decode_jwt_valid_token(test_data):
    """
    Confirm 'decode_jwt' returns the correct payload for a valid token.
    """
    token = create_jwt(test_data)
    decoded_data = decode_jwt(token)
    
    assert decoded_data["user_id"] == test_data["user_id"]
    assert decoded_data["username"] == test_data["username"]


def test_decode_jwt_expired_token(test_data):
    """
    Ensure 'decode_jwt' raises HTTPException for an expired token.
    """
    expired_token = create_jwt(test_data, expires_delta=timedelta(seconds=-1))  # Immediate expiration
    
    with pytest.raises(HTTPException) as exc_info:
        decode_jwt(expired_token)
    assert exc_info.value.detail == "Token expired"


def test_decode_jwt_invalid_token():
    """
    Verify 'decode_jwt' raises HTTPException for an invalid token.
    """
    invalid_token = "this.is.an.invalid.token"
    
    with pytest.raises(HTTPException) as exc_info:
        decode_jwt(invalid_token)
    assert exc_info.value.detail == "Invalid token"
