from app.core.config import settings


def test_search_workers_returns_result(worker_client):
    # Set up

    # Exercise
    response = worker_client.get(f"{settings.API_V1_STR}/workers/")
    data = response.json()

    # Verify
    assert response.status_code == 200
    for i in range(5):
        assert data[i]["username"] == f"Worker{i+1}"
        assert data[i]["id"] == i + 1


def test_fetch_worker_returns_result(worker_client):
    # Set up

    # Exercise
    response = worker_client.get(f"{settings.API_V1_STR}/workers/1")
    data = response.json()

    # Verify
    assert response.status_code == 200
    assert data["username"] == "Worker1"
    assert data["id"] == 1


def test_fetch_worker_returns_404(no_result_client):
    # Set up

    # Exercise
    response = no_result_client.get(f"{settings.API_V1_STR}/workers/1")

    # Verify
    assert response.status_code == 404


def test_create_worker_returns_201(no_result_client):
    # Set up
    body = {"id": 1, "username": "Worker1"}

    # Exercise
    response = no_result_client.post(f"{settings.API_V1_STR}/workers/", json=body)

    # Verify
    # The fixture returns a result
    assert response.status_code == 201


def test_create_worker_returns_400(worker_client):
    # Set up
    body = {"id": 1, "username": "Worker1"}

    # Exercise
    response = worker_client.post(f"{settings.API_V1_STR}/workers/", json=body)

    # Verify
    # The fixture returns a result
    assert response.status_code == 400


def test_delete_worker_returns_200(worker_client):
    # Set up

    # Exercise
    response = worker_client.delete(f"{settings.API_V1_STR}/workers/1")

    # Verify
    # The fixture returns a result
    assert response.status_code == 200


def test_delete_worker_returns_404(no_result_client):
    # Set up

    # Exercise
    response = no_result_client.delete(f"{settings.API_V1_STR}/workers/1")

    # Verify
    # The fixture returns no result
    assert response.status_code == 404


def test_add_shift_to_worker_returns_200(worker_shift_client):
    # Set up
    body = {}

    # Exercise
    response = worker_shift_client.post(
        f"{settings.API_V1_STR}/workers/1/shifts/1", json=body
    )

    # Verify
    # The fixture returns no result
    assert response.status_code == 200


def test_add_shift_to_worker_returns_404(no_result_client):
    # Set up
    body = {}

    # Exercise
    response = no_result_client.post(
        f"{settings.API_V1_STR}/workers/1/shifts/1", json=body
    )

    # Verify
    # The fixture returns no result
    assert response.status_code == 404


def test_add_shift_to_worker_returns_409(worker_shift_add_error_client):
    # Set up
    body = {}

    # Exercise
    response = worker_shift_add_error_client.post(
        f"{settings.API_V1_STR}/workers/1/shifts/1", json=body
    )

    # Verify
    # The fixture returns no result
    assert response.status_code == 409


def test_delete_shift_from_worker_returns_200(worker_shift_delete_client):
    # Set up

    # Exercise
    response = worker_shift_delete_client.delete(
        f"{settings.API_V1_STR}/workers/1/shifts/1"
    )

    # Verify
    # The fixture returns no result
    assert response.status_code == 200


def test_delete_shift_from_worker_returns_404(worker_shift_delete_error_client):
    # Set up

    # Exercise
    response = worker_shift_delete_error_client.delete(
        f"{settings.API_V1_STR}/workers/1/shifts/1"
    )

    # Verify
    # The fixture returns no result
    assert response.status_code == 404
