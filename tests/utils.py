from app.schemas.user import UserSignUp


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
