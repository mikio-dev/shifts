from app.core.config import settings


def test_search_managers_returns_result(manager_client):
    # Set up

    # Exercise
    response = manager_client.get(f"{settings.API_V1_STR}/managers/")
    data = response.json()

    # Verify
    assert response.status_code == 200
    for i in range(5):
        assert data[i]["username"] == f"Manager{i+1}"
        assert data[i]["id"] == i + 1


def test_fetch_manager_returns_result(manager_client):
    # Set up

    # Exercise
    response = manager_client.get(f"{settings.API_V1_STR}/managers/1")
    data = response.json()

    # Verify
    assert response.status_code == 200
    assert data["username"] == "Manager1"
    assert data["id"] == 1


def test_fetch_manager_returns_404(no_result_client):
    # Set up

    # Exercise
    response = no_result_client.get(f"{settings.API_V1_STR}/managers/1")

    # Verify
    assert response.status_code == 404


def test_create_manager_returns_201(no_result_client):
    # Set up
    body = {"id": 1, "username": "Manager1"}

    # Exercise
    response = no_result_client.post(f"{settings.API_V1_STR}/managers/", json=body)

    # Verify
    # The fixture returns a result
    assert response.status_code == 201


def test_create_manager_returns_400(manager_client):
    # Set up
    body = {"id": 1, "username": "Manager1"}

    # Exercise
    response = manager_client.post(f"{settings.API_V1_STR}/managers/", json=body)

    # Verify
    # The fixture returns a result
    assert response.status_code == 400


def test_delete_manager_returns_200(manager_client):
    # Set up

    # Exercise
    response = manager_client.delete(f"{settings.API_V1_STR}/managers/1")

    # Verify
    # The fixture returns a result
    assert response.status_code == 200


def test_delete_manager_returns_404(no_result_client):
    # Set up

    # Exercise
    response = no_result_client.delete(f"{settings.API_V1_STR}/managers/1")

    # Verify
    # The fixture returns no result
    assert response.status_code == 404
