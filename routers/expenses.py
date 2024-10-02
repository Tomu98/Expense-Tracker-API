from fastapi import APIRouter, HTTPException, status, Path
from dependencies.database import db_dependency
from dependencies.auth import user_dependency
from models.expense import Expense
from schemas.expense import AddExpense, UpdateExpense
from datetime import date, timedelta



router = APIRouter(
    tags=["Expenses"]
)



# Read all expenses
@router.get("/expenses", status_code=status.HTTP_200_OK)
async def read_expenses(
    user: user_dependency,
    db: db_dependency,
    start_date: date = None,
    end_date: date = None,
    period: str = None
):
    """
    Read expenses with optional date filters.

    - **start_date**: Optional. The starting date in 'YYYY-MM-DD' format.
    - **end_date**: Optional. The ending date in 'YYYY-MM-DD' format.
    - **period**: Optional. Can be 'week', 'month', or '3months' to filter expenses in the respective period.
    """
    query = db.query(Expense).filter(Expense.user_id == user.id)
    
    if period:
        period_map = {
            "week": timedelta(days=7),
            "month": timedelta(days=30),
            "3months": timedelta(days=90)
        }
        if period in period_map:
            start_date = date.today() - period_map[period]
            end_date = date.today()
    
    if start_date:
        query = query.filter(Expense.date >= start_date)
    if end_date:
        query = query.filter(Expense.date <= end_date)

    expenses = query.order_by(Expense.id).all()
    return {"expenses": expenses}



# Add expense
@router.post("/expenses", status_code=status.HTTP_201_CREATED)
async def add_expense(user: user_dependency, expense: AddExpense, db: db_dependency):
    new_expense = Expense(
        user_id=user.id,
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
@router.put("/expenses/{id}", status_code=status.HTTP_200_OK)
async def update_expense(user: user_dependency, expense: UpdateExpense, db: db_dependency, id: int = Path(gt=0)):
    check_expense = db.query(Expense).filter(Expense.id == id, Expense.user_id == user.id).first()

    if not check_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The expense doesn't exist.")

    for key, value in vars(expense).items():
        if value is not None:
            setattr(check_expense, key, value)

    db.add(check_expense)
    db.commit()
    return {"message": f"Expense with ID {id} successfully updated."}



# Delete expense
@router.delete("/expenses/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(user: user_dependency, id: int, db: db_dependency):
    to_delete = db.query(Expense).filter(Expense.id == id, Expense.user_id == user.id).first()

    if not to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The expense doesn't exist or you don't have permission to delete it.")

    db.delete(to_delete)
    db.commit()
