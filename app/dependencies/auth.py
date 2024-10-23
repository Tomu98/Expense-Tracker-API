from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.dependencies.database import db_dependency
from app.dependencies.jwt import decode_jwt
from app.models.user import User
from passlib.context import CryptContext
from typing import Annotated
from jose import JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes a plaintext password using bcrypt.

    Args:
        password (str): Plaintext password to be hashed.

    Returns:
        str: Hashed password.
    """
    return bcrypt_context.hash(password)



def authenticate_user(username: str, password: str, db: db_dependency):
    """
    Authenticates a user by verifying their username and password.

    Args:
        username (str): The username to authenticate.
        password (str): The plaintext password provided by the user.
        db (db_dependency): Database session dependency.

    Returns:
        User or bool: The authenticated user object if credentials are valid, False otherwise.
    """
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False

    if not bcrypt_context.verify(password, user.hashed_password):
        return False

    return user



def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    """
    Retrieves the current user based on the provided JWT token.

    Args:
        token (Annotated[str, Depends): The JWT token used for authentication.
        db (db_dependency): Database session dependency.

    Raises:
        HTTPException: If the token is invalid, expired, or the user cannot be found.

    Returns:
        User: The authenticated user object.
    """
    try:
        payload = decode_jwt(token)
        user_id: int = payload.get("id")
        username: str = payload.get("sub")

        if user_id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")

        return user

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or token expired.")


user_dependency = Annotated[User, Depends(get_current_user)]
