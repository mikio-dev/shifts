def test_delete_manager_deletes_manager(client):

    # Expected output
    # {
    #     "username": "Manager1",
    #     "id": 2,
    # }

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/managers/2"

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
    assert res.text == "2"


def test_delete_different_manager_returns_401(client):

    # Expected output
    # {'detail': 'Not authorized'}

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/managers/1"

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Manager1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.delete(url=url, headers=headers)

    # Verify
    res_json = res.json()
    print(res_json)
    assert res.status_code == 401
    assert res_json["detail"] == "Not authorized"


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


def test_delete_manager_without_login_returns_401(client):

    # Expected output
    # {"detalis": "Not authenticated"}

    # Set up
    session, api_url = client
    url = f"{api_url}/managers/2"

    # Exercise
    res = session.delete(url=url)
    res_json = res.json()

    # Verify
    assert res.status_code == 401
    assert res_json["detail"] == "Not authenticated"
