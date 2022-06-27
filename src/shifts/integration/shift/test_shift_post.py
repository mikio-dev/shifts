from datetime import date, timedelta


def test_post_shift_without_login_returns_401(client):

    # Input
    # {
    #   "shift_date": "2022-06-24",
    #   "shift_slot": 1
    # }
    #
    # Expected output
    # {
    #   "detail": "Not authenticated"
    # }

    # Set up
    session, api_url = client
    url = f"{api_url}/shifts/"
    shift_date = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")
    shift_slot = 1
    data = {"shift_date": shift_date, "shift_slot": shift_slot}

    # Exercise
    res = session.post(url=url, json=data)

    # Verify
    res_json = res.json()
    assert res.status_code == 401
    assert res_json["detail"] == "Not authenticated"


def test_post_shift_creates_shift(client):

    # Input
    # {
    #   "shift_date": "2022-06-24",
    #   "shift_slot": 1
    # }
    #
    # Expected output
    # {
    #   "id": 22,
    #   "shift_date": "2022-06-24",
    #   "shift_slot": 1
    # }

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/shifts/"
    shift_date = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")
    shift_slot = 1
    shift_dict = {"shift_date": shift_date, "shift_slot": shift_slot}

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Manager1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.post(url=url, json=shift_dict, headers=headers)

    # Verify
    res_json = res.json()
    assert res.status_code == 201
    assert res_json["id"] == 22
    assert res_json["shift_date"] == shift_date
    assert res_json["shift_slot"] == shift_slot


def test_post_shift_by_worker_returns_401(client):

    # Input
    # {
    #   "shift_date": "2022-06-24",
    #   "shift_slot": 1
    # }
    #
    # Expected output
    # {
    #   "detail": "Not authorized"
    # }

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/shifts/"
    shift_date = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")
    shift_slot = 1
    shift_dict = {"shift_date": shift_date, "shift_slot": shift_slot}

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Worker1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.post(url=url, json=shift_dict, headers=headers)

    # Verify
    res_json = res.json()
    assert res.status_code == 401
    assert res_json["detail"] == "Not authorized"


def test_post_same_shift_returns_400(client):

    # Input
    # {
    #   "shift_date": "2022-06-24",
    #   "shift_slot": 1
    # }
    #
    # Expected output
    # {'detail': 'Shift already exists'}

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/shifts/"
    shift_date = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")
    shift_slot = 1
    shift_dict = {"shift_date": shift_date, "shift_slot": shift_slot}

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Manager1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.post(url=url, json=shift_dict, headers=headers)
    # Try to create the same shift again
    res = session.post(url=url, json=shift_dict, headers=headers)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 400
    assert res_json["detail"] == "Shift already exists"


def test_post_wrong_shift_slot_returns_422(client):

    # Input
    # {
    #   "shift_date": "2022-07-01",
    #   "shift_slot": 4
    # }
    #
    # Expected output
    # {'detail': [
    #   {
    #       'ctx': {'enum_values': [1, 2, 3]},
    #       'loc': ['body', 'shift_slot'],
    #       'msg': 'value is not a valid enumeration member; permitted: 1, 2, 3',
    #       'type': 'type_error.enum'
    #   }
    # ]}

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/shifts/"
    shift_date = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")
    shift_slot = 4
    shift_dict = {"shift_date": shift_date, "shift_slot": shift_slot}

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Manager1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.post(url=url, json=shift_dict, headers=headers)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 422
    assert res_json["detail"][0]["type"] == "type_error.enum"
    assert "shift_slot" in res_json["detail"][0]["loc"]
    assert res_json["detail"][0]["ctx"]["enum_values"] == [1, 2, 3]
