from fastapi import APIRouter
from starlette import status
from schemas.user import UserSignUp, UserLogin

router = APIRouter()


# Sign up
@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def register(user: UserSignUp):
    return {"message": f"Sign up as {user}"}

# Login
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin):
    return {"message": f"Login in as {user}"}
