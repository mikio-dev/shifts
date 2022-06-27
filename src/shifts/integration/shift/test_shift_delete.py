def test_delete_shift_without_login_returns_401(client):

    # Expected output
    # {
    #   "detail": "Not authenticated"
    # }

    # Set up
    session, api_url = client
    url = f"{api_url}/shifts/1"

    # Exercise
    res = session.delete(url=url)

    # Verify
    res_json = res.json()
    assert res.status_code == 401
    assert res_json["detail"] == "Not authenticated"


def test_delete_shift_deletes_shift(client):

    # Expected output
    # {
    #     "username": "shift1",
    #     "id": 1,
    # }

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/shifts/1"

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


def test_delete_shift_by_worker_returns_401(client):

    # Expected output
    # {
    #   "detail": "Not authorized"
    # }

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/shifts/1"

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


def test_delete_non_existent_shift_returns_404(client):

    # Expected output
    # {'detail': 'Not Found'}

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/shift/100"

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
    print(res_json)
    assert res.status_code == 404
    assert res_json["detail"] == "Not Found"
