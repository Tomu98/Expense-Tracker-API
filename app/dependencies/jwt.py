import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone


# Load environment variables
load_dotenv()


# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


# Ensure the SECRET_KEY is available
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is missing")



def create_jwt(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    """
    Creates a JWT token with the provided data and expiration time.

    Args:
        data (dict): The payload to encode into the JWT.
        expires_delta (timedelta, optional): The amount of time before the token expires. Defaults to timedelta(minutes=30).

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def decode_jwt(token: str) -> dict:
    """
    Decodes a JWT token and verifies its validity.

    Args:
        token (str): The JWT token to decode.

    Raises:
        HTTPException: If the token has expired or is otherwise invalid.

    Returns:
        dict: The decoded token payload.
    """
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
