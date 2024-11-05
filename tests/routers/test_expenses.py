from fastapi import status
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

    response_data = response.json()
    expenses = response_data.get("expenses", response_data)

    assert len(expenses) > 0

    for expense in expenses:
        assert 'date' in expense



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
    expense_response = create_expense_for_test(client, auth_user_token, 50.0, "Utilities", "Test expense")
    expense_id = expense_response["id"]

    invalid_update_data = {"category": "InvalidCategory"}
    response = client.put(f"/expenses/{expense_id}", json=invalid_update_data, headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    error_message = response.json()["detail"][0]["msg"]
    assert "Invalid category" in error_message
    assert "Allowed categories are:" in error_message



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
