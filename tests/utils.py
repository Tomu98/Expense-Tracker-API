from app.schemas.expense import AddExpense
from app.schemas.user import UserSignUp
from datetime import date



def create_user_for_test(client, username, email, password):
    """
    Create a user for testing purposes.

    Args:
        client (TestClient): Test client for API requests.
        username (str): The username for the new user.
        email (EmailStr): The email for the new user.
        password (str): The password for the new user.

    Returns:
        response: The response from the signup endpoint.
    """
    user_data = UserSignUp(
        username=username,
        email=email,
        password=password,
        confirm_password=password
    ).model_dump()  # Serialize user data

    return client.post("/signup", json=user_data)


def create_expense_for_test(client, token, amount, category, description):
    """
    Create an expense for testing purposes.

    Args:
        client (TestClient): The test client used for making API requests.
        token (str): The authorization token for the authenticated user.
        amount (float): The amount for the new expense.
        category (str): The category of the expense.
        description (str): A description for the expense.

    Returns:
        response: The response from the expenses endpoint.
    """
    expense_data = AddExpense(
        amount=amount,
        category=category,
        description=description,
        date=date.today()
    ).model_dump()  # Serialize expense data

    # Convert date to string in format 'YYYYY-MM-DD'.
    expense_data['date'] = expense_data['date'].isoformat()

    return client.post("/expenses", json=expense_data, headers={"Authorization": f"Bearer {token}"})

# Asegurate que al cambiar lo primero sobre el formato str, no se joda todo
