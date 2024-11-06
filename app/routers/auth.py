from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.auth import authenticate_user, hash_password
from app.dependencies.database import db_dependency
from app.dependencies.jwt import create_jwt
from app.models.user import User
from app.schemas.user import UserSignUp, Token
from datetime import timedelta


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signup", summary="User Registration", status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignUp, db: db_dependency):
    """
    ***Register a new user.***

    **Args:**
        user (UserSignUp): Schema containing the user's registration details (username, email, and password).
        db (db_dependency): Database session used to check existing users and register the new user.

    **Raises:**
        HTTPException: If the `email` is already registered.
        HTTPException: If the `username` is already taken.

    **Returns:**
        dict: A message confirming the registration and the user's ID.
    """
    check_email = db.query(User).filter(User.email == user.email).first()
    check_username = db.query(User).filter(User.username == user.username).first()

    if check_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")

    if check_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken.")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"detail": f"User '{new_user.username}' successfully registered", "id": new_user.id}



@router.post("/login", summary="User Login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    ***Authenticate a user and return a JWT token.***

    **Args:**
        db (db_dependency): Database session used to verify the user's credentials.
        form_data (OAuth2PasswordRequestForm, optional): Contains the username and password submitted by the user. Defaults to Depends().

    **Raises:**
        HTTPException: If the provided credentials are invalid.

    **Returns:**
        dict: A dictionary with the access token and its type ("bearer").
    """
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    token_expires = timedelta(minutes=30)
    token = create_jwt({"sub": user.username, "id": user.id}, expires_delta=token_expires)

    return {"access_token": token, "token_type": "bearer"}
