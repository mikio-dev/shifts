from datetime import date, timedelta


def test_post_worker_creates_worker(client):

    # Input
    # {
    #   "username": "Worker2"
    # }
    #
    # Expected output
    # {
    #     "username": "Worker2",
    #     "id": 3,
    #     "shifts": []
    # }

    # Set up
    session, api_url = client
    url = f"{api_url}/workers/"
    username = "Worker2"
    data = {"username": username}

    # Exercise
    res = session.post(url=url, json=data)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 201
    assert res_json["id"] == 3
    assert res_json["username"] == username
    assert res_json["shifts"] == []


def test_post_same_worker_returns_400(client):

    # Input
    # {
    #   "username": "Worker2"
    # }
    #
    # Expected output
    # {'detail': 'Username already registered'}

    # Set up
    session, api_url = client
    url = f"{api_url}/workers/"
    username = "Worker2"
    data = {"username": username}

    # Exercise
    res = session.post(url=url, json=data)
    # Try to create the same worker again
    res = session.post(url=url, json=data)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 400
    assert res_json["detail"] == "Username already registered"


def test_post_shift_for_worker_add_shift(client):

    # Expected output
    # {
    #   "worker_id": 1,
    #   "shift_id": 4,
    #   "shift_date": "2022-06-25"
    # }

    # Set up
    session, api_url = client
    shift_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    url_worker = f"{api_url}/workers/1"
    url_shift = f"{url_worker}/shifts/4"

    # Exercise
    res_shift = session.post(url=url_shift)
    res_worker = session.get(url=url_worker)

    # Verify
    res_shift_json = res_shift.json()
    assert res_shift.status_code == 200
    assert res_shift_json["worker_id"] == 1
    assert res_shift_json["shift_id"] == 4
    assert res_shift_json["shift_date"] == shift_date

    res_worker_json = res_worker.json()

    assert res_worker.status_code == 200
    assert res_worker_json["id"] == 1
    assert res_worker_json["username"] == "Worker1"
    assert res_worker_json["shifts"][1]["worker_id"] == 1
    assert res_worker_json["shifts"][1]["shift_id"] == 4
    assert res_worker_json["shifts"][1]["shift_date"] == shift_date


def test_post_shift_on_the_same_day_returns_409(client):

    # Expected output
    # {'detail': "Worker already has a Shift on the specified date.{'worker_id': 1, 'shift_date': '2022-06-24', 'shift_slot': 1}"
    # }

    # Set up
    session, api_url = client
    url = f"{api_url}/workers/1/shifts/2"

    # Exercise
    res = session.post(url=url)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 409
    assert "Worker already has a Shift on the specified date" in res_json["detail"]
