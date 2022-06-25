from datetime import date, timedelta


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
    url = f"{api_url}/shifts/"
    shift_date = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")
    shift_slot = 1
    data = {"shift_date": shift_date, "shift_slot": shift_slot}

    # Exercise
    res = session.post(url=url, json=data)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 201
    assert res_json["id"] == 22
    assert res_json["shift_date"] == shift_date
    assert res_json["shift_slot"] == shift_slot


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
    url = f"{api_url}/shifts/"
    shift_date = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")
    shift_slot = 1
    data = {"shift_date": shift_date, "shift_slot": shift_slot}

    # Exercise
    res = session.post(url=url, json=data)
    # Try to create the same shift again
    res = session.post(url=url, json=data)

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
    url = f"{api_url}/shifts/"
    shift_date = (date.today() + timedelta(days=8)).strftime("%Y-%m-%d")
    shift_slot = 4
    data = {"shift_date": shift_date, "shift_slot": shift_slot}

    # Exercise
    res = session.post(url=url, json=data)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 422
    assert res_json["detail"][0]["type"] == "type_error.enum"
    assert "shift_slot" in res_json["detail"][0]["loc"]
    assert res_json["detail"][0]["ctx"]["enum_values"] == [1, 2, 3]
