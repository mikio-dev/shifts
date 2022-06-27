from datetime import date, timedelta


def test_delete_worker_deletes_worker(client):

    # Expected output
    # {
    #     "username": "Worker1",
    #     "id": 1,
    # }

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/workers/1"

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Manager1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.delete(url=url, headers=headers)

    # Verify
    assert res.status_code == 200
    assert res.text == "1"


def test_delete_worker_by_worker_returns_401(client):

    # Expected output
    # {'detail': 'Not authorized'}

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/workers/1"

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Worker1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.delete(url=url, headers=headers)

    # Verify
    res_json = res.json()
    assert res.status_code == 401
    assert res_json["detail"] == "Not authorized"


def test_delete_worker_without_login_returns_401(client):

    # Expected output
    # {"detalis": "Not authenticated"}

    # Set up
    session, api_url = client
    url = f"{api_url}/workers/1"

    # Exercise
    res = session.delete(url=url)
    res_json = res.json()

    # Verify
    assert res.status_code == 401
    assert res_json["detail"] == "Not authenticated"


def test_delete_shift_without_login_returns_401(client):

    # Expected output
    # {"detalis": "Not authenticated"}

    # Set up
    session, api_url = client
    url = f"{api_url}/workers/1/shifts/1"

    # Exercise
    res = session.delete(url=url)
    res_json = res.json()

    # Verify
    assert res.status_code == 401
    assert res_json["detail"] == "Not authenticated"


def test_delete_shift_from_worker_deletes_shift(client):

    # Expected output
    # {
    #   "worker_id": 1,
    #   "shift_id": 1,
    #   "shift_date": "2022-06-24"
    # }

    # Set up
    session, api_url = client

    url_login = f"{api_url}/auth/login"
    url_shift = f"{api_url}/workers/1/shifts/1"

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Worker1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res_shift = session.delete(url=url_shift, headers=headers)

    # Verify
    res_shift_json = res_shift.json()
    assert res_shift.status_code == 200
    assert res_shift_json["worker_id"] == 1
    assert res_shift_json["shift_id"] == 1
    assert res_shift_json["shift_date"] == date.today().strftime("%Y-%m-%d")


def test_delete_shift_from_different_worker_returns_401(client):

    # Expected output
    # {"detalis": "Not authorized"}

    # Set up
    session, api_url = client

    url_login = f"{api_url}/auth/login"
    url_shift = f"{api_url}/workers/2/shifts/1"

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Worker1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res_shift = session.delete(url=url_shift, headers=headers)

    # Verify
    res_shift_json = res_shift.json()
    assert res_shift.status_code == 401
    assert res_shift_json["detail"] == "Not authorized"
