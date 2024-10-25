from fastapi import status
from tests.test_utils import create_user_for_test



def test_update_username_not_authenticated(client):
    response = client.put("/update", json={"username": "newusername"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_update_username_not_found(client):
    pass


def test_update_username_conflict(client):
    response1 = create_user_for_test(client, "user1", "user1@example.com", "password1")
    assert response1.status_code == status.HTTP_201_CREATED

    response2 = create_user_for_test(client, "user2", "user2@example.com", "password2")
    assert response2.status_code == status.HTTP_201_CREATED

    # Login as the second user
    login_response = client.post("/login", data={"username": "user1", "password": "password1"})
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]

    # Attempt to update the username of the second user to the existing username
    update_response = client.put(
        "/update",
        json={"username": "user2"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_response.status_code == status.HTTP_400_BAD_REQUEST
    assert update_response.json() == {"detail": "Username already in use."}


def test_update_username_success(client):
    response = create_user_for_test(client, "originaluser", "original@example.com", "testpassword")
    assert response.status_code == status.HTTP_201_CREATED
    
    login_response = client.post("/login", data={"username": "originaluser", "password": "testpassword"})
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    
    update_response = client.put(
        "/update",
        json={"username": "updateduser"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert update_response.status_code == status.HTTP_200_OK
    assert update_response.json() == {"msg": "Username updated successfully.", "username": "updateduser"}
