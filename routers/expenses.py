from fastapi import APIRouter, HTTPException, status
from dependencies.database import db_dependency
from models.expense import Expense
from schemas.expense import AddExpense, UpdateExpense


router = APIRouter(
    tags=["Expenses"]
)



# Read all expenses
@router.get("/expenses")
async def read_all_expenses(db: db_dependency):
    expenses = db.query(Expense).all()
    return {"expenses": expenses}



# Add expense
@router.post("/expenses")
async def add_expense(expense: AddExpense, db: db_dependency):
    new_expense = Expense(
        user_id=expense.user_id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date
    )
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return {"message": f"Expense ${new_expense.amount} added.", "id": new_expense.id}



# Update expense
@router.put("/expenses/{id}")
async def update_expense(expense: UpdateExpense, id: int, db: db_dependency):
    check_expense = db.query(Expense).filter(Expense.id == id).first()

    if not check_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The expense doesn't exist.")

    for key, value in vars(expense).items():
        if value is not None:
            setattr(check_expense, key, value)

    db.commit()
    return {"message": f"Expense with ID {id} successfully updated."}



# Delete expense
@router.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(id: int, db: db_dependency):
    to_delete = db.query(Expense).filter(Expense.id == id).first()

    if not to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The expense doesn't exist.")

    db.delete(to_delete)
    db.commit()

# En addexpense, creo que tengo que obtener el id del usuario que inició sesión
# Hacer que todos estos endpoints solo se vean al iniciar sesión
