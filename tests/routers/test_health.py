from fastapi import status


def test_return_health_check(client):
    """
    Test the health check endpoint to ensure the server is operational.
    """
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'Healthy'}
