from fastapi import APIRouter, HTTPException, status
from dependencies.database import db_dependency


router = APIRouter()


# Actualizar perfil
@router.put("/update", status_code=status.HTTP_201_CREATED)
async def update_account(db: db_dependency):
    pass

# Eliminar cuenta
@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(db: db_dependency):
    pass
