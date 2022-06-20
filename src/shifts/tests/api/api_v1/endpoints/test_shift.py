import pytest

from app.core.config import settings

def test_search_shifts_returns_result(shift_client):
    # Set up

    # Exercise
    response = shift_client.get(f"{settings.API_V1_STR}/shifts/")
    data = response.json()

    # Verify
    assert response.status_code == 200
    for i in range(5):
        assert data[i]["id"] == i + 1
        assert data[i]["shift_date"] == f"2022-01-0{i+1}"
        assert data[i]["shift_slot"] == i % 3 + 1


def test_fetch_shift_returns_result(shift_client):
    # Set up

    # Exercise
    response = shift_client.get(f"{settings.API_V1_STR}/shifts/1")
    data = response.json()

    # Verify
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["shift_date"] == "2022-01-01"
    assert data["shift_slot"] == 1


def test_fetch_shift_returns_404(no_result_client):
    # Set up

    # Exercise
    response = no_result_client.get(f"{settings.API_V1_STR}/shifts/1")

    # Verify
    assert response.status_code == 404


def test_create_shift_returns_201(no_result_client):
    # Set up
    body = {"id": 1, "shift_date": "2022-01-01", "shift_slot": 1}

    # Exercise
    response = no_result_client.post(f"{settings.API_V1_STR}/shifts/", json=body)

    # Verify
    # The fixture returns a result
    assert response.status_code == 201


def test_create_shift_returns_400(shift_client):
    # Set up
    body = {"id": 1, "shift_date": "2022-01-01", "shift_slot": 1}

    # Exercise
    response = shift_client.post(f"{settings.API_V1_STR}/shifts/", json=body)

    # Verify
    # The fixture returns a result
    assert response.status_code == 400

@pytest.mark.parametrize('invalid_shift_slot', [0, 4, 5])
def test_create_shift_returns_422_with_wrong_shift_slot(no_result_client, invalid_shift_slot):
    # Set up
    body = {"id": 1, "shift_date": "2022-01-01", "shift_slot": invalid_shift_slot}

    # Exercise
    response = no_result_client.post(f"{settings.API_V1_STR}/shifts/", json=body)

    # Verify
    # The fixture returns a result
    assert response.status_code == 422


def test_delete_shift_returns_200(shift_client):
    # Set up

    # Exercise
    response = shift_client.delete(f"{settings.API_V1_STR}/shifts/1")

    # Verify
    # The fixture returns a result
    assert response.status_code == 200


def test_delete_shift_returns_404(no_result_client):
    # Set up

    # Exercise
    response = no_result_client.delete(f"{settings.API_V1_STR}/shifts/1")

    # Verify
    # The fixture returns no result
    assert response.status_code == 404
