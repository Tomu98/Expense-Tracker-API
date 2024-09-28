import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone


load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is missing")



def create_jwt(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    # Copy of the data dictionary
    to_encode = data.copy()

    # Token expiration date
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})

    # Encrypt token with secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def decode_jwt(token: str):
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token claims")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
