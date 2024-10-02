from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from dependencies.database import db_dependency
from dependencies.jwt import create_jwt
from dependencies.auth import authenticate_user, hash_password
from models.user import User
from schemas.user import UserSignUp, Token
from datetime import timedelta



router = APIRouter(
    tags=["Authentication"]
)



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

    return {"detail": f"User '{new_user.username}' successfully registered", "id": new_user.id}



# Login
@router.post("/login", response_model=Token,status_code=status.HTTP_200_OK)
async def login_for_access_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    
    token_expires = timedelta(minutes=30)
    token = create_jwt({"sub": user.username, "id": user.id}, expires_delta=token_expires)
    
    return {"access_token": token, "token_type": "bearer"}
