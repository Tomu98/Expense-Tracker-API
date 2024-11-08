import pytest
from fastapi import status
from datetime import date, timedelta
from tests.utils import create_expense_for_test



# Tests for reading expenses
def test_read_expenses_no_data(client, auth_user_token):
    """
    Verify response when no expenses exist.
    """
    response = client.get("/expenses", headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"expenses": []}


def test_read_expenses_with_data(client, auth_user_token):
    """
    Check retrieval of expenses with data present.
    """
    create_expense_for_test(client, auth_user_token, 50.0, "Utilities", "Test expense")

    response = client.get("/expenses", headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_200_OK

    expenses = response.json().get("expenses", [])
    assert len(expenses) > 0

    for expense in expenses:
        assert all(key in expense for key in ["amount", "category", "description", "date"])


def test_read_expenses_date_range_filter(client, auth_user_token):
    """
    Verify expenses are filtered correctly within a specific date range.
    """
    today = date.today()
    yesterday = today - timedelta(days=1)

    create_expense_for_test(client, auth_user_token, 20.0, "Groceries", "Expense Today", today)
    create_expense_for_test(client, auth_user_token, 10.0, "Health", "Expense Yesterday", yesterday)

    from_date = yesterday.isoformat()
    to_date = (today + timedelta(days=1)).isoformat()

    response = client.get(f"/expenses?from_date={from_date}&to_date={to_date}", headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_200_OK

    expenses = response.json().get("expenses", [])
    assert len(expenses) == 2

    for expense in expenses:
        assert from_date <= expense["date"] <= to_date


@pytest.mark.parametrize("period,expected_count", [("week", 2), ("month", 2), ("3months", 2)])
def test_read_expenses_period_filter(client, auth_user_token, period, expected_count):
    """
    Test filtering expenses based on a specified period.
    """
    today = date.today()
    expenses_data = [
        (30.0, "Leisure", "Expense Yesterday", today - timedelta(days=1)),
        (15.0, "Electronics", "Expense Last Week", today - timedelta(days=7)),
    ]

    for amount, category, description, expense_date in expenses_data:
        create_expense_for_test(client, auth_user_token, amount, category, description, expense_date)

    response = client.get(f"/expenses?period={period}", headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_200_OK

    expenses = response.json().get("expenses", [])
    assert len(expenses) == expected_count

    # Validate that the dates of expenses are within the expected range
    for expense in expenses:
        expense_date = date.fromisoformat(expense["date"].split("T")[0])
        assert today - timedelta(days=90) <= expense_date <= today


def test_read_expenses_invalid_period(client, auth_user_token):
    """
    Verify response for an invalid period parameter.
    """
    response = client.get("/expenses?period=invalid", headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid 'period' value" in response.json().get("detail", "")


def test_read_expenses_order(client, auth_user_token):
    """
    Ensure expenses are returned in descending order by date.
    """
    today = date.today()
    two_days_ago = today - timedelta(days=2)
    yesterday = today - timedelta(days=1)

    create_expense_for_test(client, auth_user_token, 40.0, "Clothing", "Expense Two Days Ago", two_days_ago)
    create_expense_for_test(client, auth_user_token, 25.0, "Utilities", "Expense Yesterday", yesterday)
    create_expense_for_test(client, auth_user_token, 60.0, "Groceries", "Expense Today", today)

    response = client.get("/expenses", headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_200_OK
    expenses = response.json().get("expenses", [])

    assert len(expenses) == 3
    assert expenses[0]["date"] >= expenses[1]["date"] >= expenses[2]["date"]



# Tests for adding expenses
def test_add_expense_valid_data(client, auth_user_token):
    """
    Validate successful addition of a new expense.
    """
    expense_data = {"amount": 75.0, "category": "Utilities", "description": "Test expense"}
    response = client.post("/expenses", json=expense_data, headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_201_CREATED
    assert "message" in response.json()
    assert "id" in response.json()


def test_add_expense_invalid_category(client, auth_user_token):
    """
    Ensure error is raised for an invalid expense category.
    """
    expense_data = {"amount": 75.0, "category": "InvalidCategory", "description": "Testing invalid category"}
    response = client.post("/expenses", json=expense_data, headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_add_expense_missing_amount(client, auth_user_token):
    """
    Confirm error response when amount is missing.
    """
    expense_data = {"category": "Groceries", "description": "Test expense"}
    response = client.post("/expenses", json=expense_data, headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



# Tests for updating expenses
def test_update_expense_valid_data(client, auth_user_token):
    """
    Validate successful update of an existing expense.
    """
    expense_id = create_expense_for_test(client, auth_user_token, 100.0, "Utilities", "Old bill")["id"]
    update_data = {"amount": 120.0, "description": "Updated electricity bill"}
    
    response = client.put(f"/expenses/{expense_id}", json=update_data, headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == f"Expense with ID {expense_id} successfully updated."


def test_update_expense_not_found(client, auth_user_token):
    """
    Check response when updating a non-existent expense.
    """
    update_data = {"amount": 120.0, "description": "Test expense"}
    response = client.put("/expenses/99999", json=update_data, headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_expense_invalid_data(client, auth_user_token):
    """
    Ensure error is raised for invalid data when updating an expense.
    """
    expense_id = create_expense_for_test(client, auth_user_token, 50.0, "Utilities", "Test expense")["id"]

    invalid_update_data = {"category": "InvalidCategory"}
    response = client.put(f"/expenses/{expense_id}", json=invalid_update_data, headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Invalid category" in response.json()["detail"][0]["msg"]



# Tests for deleting expenses
def test_delete_expense_valid(client, auth_user_token):
    """
    Validate successful deletion of an expense.
    """
    expense_id = create_expense_for_test(client, auth_user_token, 50.0, "Others", "Test expense")["id"]

    response = client.delete(f"/expenses/{expense_id}", headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_expense_not_found(client, auth_user_token):
    """
    Check response when trying to delete a non-existent expense.
    """
    response = client.delete("/expenses/99999", headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_404_NOT_FOUND
