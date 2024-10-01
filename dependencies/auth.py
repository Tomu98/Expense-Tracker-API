from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dependencies.database import db_dependency
from dependencies.jwt import decode_jwt
from models.user import User
from jose import JWTError
from typing import Annotated
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Encrypt password function
def hash_password(password: str) -> str:
    return bcrypt_context.hash(password)



def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user



def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
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
