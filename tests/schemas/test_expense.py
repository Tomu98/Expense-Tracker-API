import pytest
from pydantic import ValidationError
from app.schemas.expense import AddExpense, UpdateExpense



# Tests for AddExpense
def test_invalid_category_add_expense():
    """
    Raise ValidationError for non-allowed category in AddExpense.
    """
    with pytest.raises(ValidationError):
        AddExpense(
            amount=100.0,
            category="InvalidCategory",
            description="Test description",
            date="2025-01-01"
        )


def test_valid_category_add_expense():
    """
    Verify AddExpense creation with a valid category.
    """
    expense = AddExpense(
        amount=100.0,
        category="Groceries",
        description="Grocery shopping",
        date="2025-01-01"
    )
    assert expense.category == "Groceries"



# Tests for UpdateExpense
def test_invalid_category_update_expense():
    """
    Ensure ValidationError for a category not in 'ALLOWED_CATEGORIES' in UpdateExpense.
    """
    with pytest.raises(ValidationError):
        UpdateExpense(
            amount=50.0,
            category="InvalidCategory",
            description="Updated description",
            date="2025-01-02"
        )


def test_valid_category_update_expense():
    """
    Verify UpdateExpense allows a valid category.
    """
    expense_update = UpdateExpense(
        amount=50.0,
        category="Health",
        description="Medical expenses",
        date="2025-01-02"
    )
    assert expense_update.category == "Health"
