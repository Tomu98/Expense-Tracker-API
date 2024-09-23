from fastapi import APIRouter

router = APIRouter()


# Read all expenses
@router.get("/expenses")
async def read_all_expenses():
    pass

# Add expense
@router.post("/expenses")
async def add_expense():
    pass

# Update expense
@router.put("/expenses/{id}")
async def update_expense(id: int):
    pass

# Delete expense
@router.delete("/expesnes/{id}")
async def delete_expense(id: int):
    pass
