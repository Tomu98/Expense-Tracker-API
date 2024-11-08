from fastapi import status
from unittest.mock import patch
from tests.utils import create_user_for_test



# Tests for /update endpoint
def test_update_account_success(client, auth_user_token):
    """
    Test that an authenticated user can successfully update their username.
    """
    update_data = {"username": "newusername"}
    response = client.put("/user", json=update_data, headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["msg"] == "Username updated successfully."
    assert response.json()["username"] == "newusername"


def test_update_account_user_not_authenticated(client):
    """
    Test that a non-authenticated user receives an error when trying to update their account.
    """
    update_data = {"username": "newusername"}
    response = client.put("/user", json=update_data)
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
        response = client.put("/user", json=update_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Not authenticated"


def test_update_account_username_taken(client, auth_user_token):
    """
    Test that an error is returned when trying to update to a username that is already taken.
    """
    create_user_for_test(client, "existinguser", "existing@example.com", "testpassword")

    update_data = {"username": "existinguser"}
    response = client.put("/user", json=update_data, headers={"Authorization": f"Bearer {auth_user_token}"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already in use."


def test_update_account_missing_fields(client, auth_user_token):
    """
    Test that an error is returned when missing fields in the update request.
    """
    response = client.put("/user", headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_account_invalid_username_format(client, auth_user_token):
    """
    Test that an error is returned if the new username doesn't meet format requirements (e.g., too short).
    """
    update_data = {"username": "x"}
    response = client.put("/user", json=update_data, headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



# Tests for /delete endpoint
def test_delete_account_success(client, auth_user_token):
    """
    Test that an authenticated user can successfully delete their account.
    """
    response = client.delete("/user", headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_account_user_not_authenticated(client):
    """
    Test that a non-authenticated user receives an error when trying to delete their account.
    """
    response = client.delete("/user")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_account_user_not_found(client):
    """
    Test that verifies that an error is returned if the user doesn't exist when trying to delete the account.
    """
    # Simulating an authenticated user
    with patch('app.dependencies.auth.get_current_user') as mock_get_current:
        mock_get_current.return_value = None

        # Trying to delete the account
        response = client.delete("/user")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Not authenticated"


def test_delete_account_no_content(client, auth_user_token):
    """
    Test that the response is 204 No Content when deleting an account successfully.
    """
    response = client.delete("/user", headers={"Authorization": f"Bearer {auth_user_token}"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
