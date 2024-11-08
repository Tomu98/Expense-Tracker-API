from fastapi import APIRouter, HTTPException, status, Depends
from app.dependencies.auth import get_current_user
from app.dependencies.database import db_dependency
from app.models.user import User
from app.schemas.user import UpdateAccount


router = APIRouter(
    tags=["User Account"]
)


# Update account
@router.put("/user", status_code=status.HTTP_200_OK)
async def update_account(user_data: UpdateAccount, db: db_dependency, current_user: User = Depends(get_current_user)):
    """
    ***Update the authenticated user's username.***

    **Args:**
        user_data (UpdateAccount): Schema with the new username.
        db (db_dependency): Database session.
        current_user (User, optional): The currently authenticated user. Defaults to Depends(get_current_user).

    **Raises:**
        HTTPException: If the user isn't found.
        HTTPException: If the new username is already taken.

    **Returns:**
        dict: A message indicating the update was successful and the updated username.
    """
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    if db.query(User).filter(User.username == user_data.username, User.id != current_user.id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use.")

    user.username = user_data.username
    db.commit()
    db.refresh(user)

    return {"msg": "Username updated successfully.", "username": user.username}



# Delete account
@router.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(db: db_dependency, current_user: User = Depends(get_current_user)):
    """
    ***Delete the authenticated user's account.***

    **Args:**
        db (db_dependency): Database session.
        current_user (User, optional): The currently authenticated user. Defaults to Depends(get_current_user).

    **Raises:**
        HTTPException: If the user isn't found.
    """
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    db.delete(user)
    db.commit()
