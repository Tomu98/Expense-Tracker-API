from fastapi import APIRouter, HTTPException, status
from schemas.user import UserSignUp, UserLogin
from dependencies.database import db_dependency
from dependencies.jwt import create_jwt
from passlib.context import CryptContext
from models.user import User


router = APIRouter(
    tags=["Authentication"]
)


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Encrypt password function
def hash_password(password: str):
    return bcrypt_context.hash(password)



# Sign up
@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def register(user: UserSignUp, db: db_dependency):
    check_user = db.query(User).filter(User.email == user.email).first()

    if check_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"detail": f"User '{new_user.username}' successfully registered"}



# Login
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: db_dependency):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not bcrypt_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    
    token = create_jwt({"user_id": db_user.id})
    
    return {"access_token": token, "token_type": "bearer"}
