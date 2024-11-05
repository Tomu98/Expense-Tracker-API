import pytest
from datetime import date
from fastapi import status
from tests.utils import create_user_for_test, create_expense_for_test


# Ver si el fixture que devuelve el token lo puedo utilizar directamente con los demas tests para users
@pytest.fixture
def auth_user_token(client):
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)

    assert response.status_code == 200, f"Failed to authenticate, status code: {response.status_code}"
    token = response.json().get("access_token")
    assert token, "Authentication failed: 'access_token' not found in response."

    return token


def test_read_expenses_no_data(client, auth_user_token):
    response = client.get("/expenses", headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"expenses": []}


def test_read_expenses_with_data(client, auth_user_token):
    create_expense_for_test(client, auth_user_token, 50.0, "Utilities", "Testing")

    response = client.get("/expenses", headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    expenses = response_data.get("expenses", response_data)

    assert len(expenses) > 0

    for expense in expenses:
        assert 'date' in expense


def test_read_expenses_with_date_filters():
    pass



def test_add_expense_valid_data():
    pass


def test_add_expense_invalid_category():
    pass


def test_add_expense_missing_amount():
    pass



def test_update_expense_valid_data():
    pass


def test_update_expense_not_found():
    pass


def test_update_expense_invalid_data():
    pass



def test_delete_expense_valid():
    pass


def test_delete_expense_not_found():
    pass


def test_delete_expense_not_authorized():
    pass
