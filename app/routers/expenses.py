from fastapi import APIRouter, HTTPException, status, Path, Query
from app.dependencies.auth import user_dependency
from app.dependencies.database import db_dependency
from app.models.expense import Expense
from app.schemas.expense import AddExpense, UpdateExpense
from datetime import date, timedelta, datetime


router = APIRouter(
    tags=["Expenses"]
)


# Read all expenses
@router.get("/expenses", status_code=status.HTTP_200_OK)
async def read_expenses(
    user: user_dependency,
    db: db_dependency,
    from_date: date = Query(None, description="Filter expenses from this date (YYYY-MM-DD)"),
    to_date: date = Query(None, description="Filter expenses up to this date (YYYY-MM-DD)"),
    period: str = Query(None, description="Predefined period: 'week', 'month', '3months'")
):
    """
    ***Retrieve all expenses for the authenticated user with optional date filters.***

    **Args:**
        user (user_dependency): The current authenticated user.
        db (db_dependency): The database session.
        from_date (date, optional): Start date to retrieve expenses from this date onward. Defaults to None.
        to_date (date, optional): End date to retrieve expenses up to this date. Defaults to None.
        period (str, optional): Predefined period to filter expenses. Accepted values are 'week', 'month', and '3months'. Defaults to None.

    **Raises:**
        HTTPException: If an invalid period is provided.

    **Returns:**
        dict: A dictionary containing a list of expenses, ordered by date in descending order.
    """
    # Date validation (in case from_date is later than to_date)
    if from_date and to_date and from_date > to_date:
        from_date, to_date = to_date, from_date

    # Base query
    query = db.query(Expense).filter(Expense.user_id == user.id)

    # Define period-based start and end dates if period is provided
    if period:
        period_map = {
            "week": timedelta(days=7),
            "month": timedelta(days=30),
            "3months": timedelta(days=90)
        }
        period_lower = period.lower()
        if period_lower in period_map:
            from_date = datetime.now().date() - period_map[period_lower]
            to_date = datetime.now().date()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid 'period' value. Accepted values are 'week', 'month', '3months'.")

    # Apply start_date and end_date filters, casting to Date for compatibility
    if from_date:
        query = query.filter(Expense.date >= from_date)
    if to_date:
        query = query.filter(Expense.date <= to_date)

    # Execute query and return ordered expenses
    expenses = query.order_by(Expense.date.desc()).all()
    return {"expenses": expenses}



# Add expense
@router.post("/expenses", status_code=status.HTTP_201_CREATED)
async def add_expense(user: user_dependency, expense: AddExpense, db: db_dependency):
    """
    ***Add a new expense for the authenticated user.***

    **Args:**
        user (user_dependency): The current authenticated user.
        expense (AddExpense): The details of the expense to be added.
        db (db_dependency): The database session.

    **Returns:**
        dict: A dictionary with a success message and the ID of the created expense.
    """
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
    """
    ***Update an existing expense for the authenticated user.***

    **Args:**
        user (user_dependency): The current authenticated user.
        expense (UpdateExpense): The details of the expense to be updated.
        db (db_dependency): The database session.
        id (int, optional): The ID of the expense to be updated. Defaults to Path(gt=0).

    **Raises:**
        HTTPException: If the expense doesn't exist or doesn't belong to the user.

    **Returns:**
        dict: A success message indicating that the expense was updated.
    """
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
    """
    ***Delete an expense for the authenticated user.***

    **Args:**
        user (user_dependency): The current authenticated user.
        id (int): The ID of the expense to be deleted.
        db (db_dependency): The database session.

    **Raises:**
        HTTPException: If the expense doesn't exist or the user doesn't have permission to delete it.
    """
    to_delete = db.query(Expense).filter(Expense.id == id, Expense.user_id == user.id).first()

    if not to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The expense doesn't exist or you don't have permission to delete it.")

    db.delete(to_delete)
    db.commit()
