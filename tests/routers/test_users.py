from fastapi import status
from unittest.mock import patch
from tests.utils import create_user_for_test


def test_update_account_success(client):
    """
    Test that an authenticated user can successfully update their username.
    """
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    # Login to get an access token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    token = response.json().get("access_token")

    # Update account with a new username
    update_data = {"username": "newusername"}
    response = client.put("/update", json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["msg"] == "Username updated successfully."
    assert response.json()["username"] == "newusername"


def test_update_account_user_not_authenticated(client):
    """
    Test that a non-authenticated user receives an error when trying to update their account.
    """
    update_data = {"username": "newusername"}
    response = client.put("/update", json=update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_account_user_not_found(client):
    """
    Test that verifies that an error is returned if the user doesn't exist when trying to update the account.
    """
    # Simulating an authenticated user
    with patch('app.dependencies.auth.get_current_user') as mock_get_current:
        mock_get_current.return_value = None

        # Trying to update the account
        update_data = {"username": "nonexistentuser"}
        response = client.put("/update", json=update_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Not authenticated"


def test_update_account_username_taken(client):
    """
    Test that an error is returned when trying to update to a username that is already taken.
    """
    create_user_for_test(client, "existinguser", "existing@example.com", "testpassword")
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    # Login with the second user
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    token = response.json().get("access_token")

    # Attempt to update username to an existing one
    update_data = {"username": "existinguser"}
    response = client.put("/update", json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already in use."


def test_update_account_missing_fields(client):
    """
    Test that an error is returned when missing fields in the update request.
    """
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    # Login to get an access token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    token = response.json().get("access_token")

    # Attempt to update without providing any data
    response = client.put("/update", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_account_invalid_username_format(client):
    """
    Test that an error is returned if the new username doesn't meet format requirements.
    """
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    # Login to get an access token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    token = response.json().get("access_token")

    # Attempt to update to an invalid username (e.g., too short)
    update_data = {"username": "x"}
    response = client.put("/update", json=update_data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



def test_delete_account_success(client):
    """
    Test that an authenticated user can successfully delete their account.
    """
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    # Login to get an access token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    token = response.json().get("access_token")

    # Attempt to delete the account
    response = client.delete("/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_account_user_not_authenticated(client):
    """
    Test that a non-authenticated user receives an error when trying to delete their account.
    """
    response = client.delete("/delete")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_account_user_not_found(client):
    """
    Test that verifies that an error is returned if the user doesn't exist when trying to delete the account.
    """
    # Simulating an authenticated user
    with patch('app.dependencies.auth.get_current_user') as mock_get_current:
        mock_get_current.return_value = None

        # Trying to delete the account
        response = client.delete("/delete")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Not authenticated"


def test_delete_account_no_content(client):
    """
    Test that the response is 204 No Content when deleting an account successfully.
    """
    create_user_for_test(client, "testuser", "test@example.com", "testpassword")

    # Log in to get an access token
    login_data = {"username": "testuser", "password": "testpassword"}
    response = client.post("/login", data=login_data)
    token = response.json().get("access_token")

    # Attempt to delete the account
    response = client.delete("/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
