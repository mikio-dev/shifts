def test_post_manager_without_login_returns_401(client):

    # Input
    # {
    #   "username": "Manager2"
    #   "password": "password1"
    # }
    #
    # Expected output
    # {
    #   "detail": "Not authenticated"
    # }

    # Set up
    session, api_url = client
    url = f"{api_url}/managers/"
    username = "Manager2"
    new_manager = {"username": username, "password": "password1"}

    # Exercise
    res = session.post(url=url, json=new_manager)

    # Verify
    res_json = res.json()
    assert res.status_code == 401
    assert res_json["detail"] == "Not authenticated"


def test_post_manager_by_worker_returns_401(client):

    # Input
    # {
    #   "username": "Manager2"
    #   "password": "password1"
    # }
    #
    # Expected output
    # {
    #     "detail": "Not authenticated"
    # }

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/managers/"
    username = "Manager2"
    new_manager = {"username": username, "password": "password1"}

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Worker1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.post(url=url, json=new_manager, headers=headers)

    # Verify
    res_json = res.json()
    assert res.status_code == 401
    assert res_json["detail"] == "Not authorized"


def test_post_manager_creates_manager(client):

    # Input
    # {
    #   "username": "Manager2"
    #   "password": "password1"
    # }
    #
    # Expected output
    # {
    #     "username": "Manager2",
    #     "id": 3,
    # }

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/managers/"
    username = "Manager2"
    new_manager = {"username": username, "password": "password1"}

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Manager1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.post(url=url, json=new_manager, headers=headers)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 201
    assert res_json["id"] == 3
    assert res_json["username"] == username
    assert "password" not in res_json


def test_post_manager_without_password_returns_422(client):

    # Input
    # {
    #   "username": "Manager2"
    # }
    #
    # Expected output
    # {'detail': [{
    #     'loc': ['body', 'password'],
    #     'msg': 'field required',
    #     'type': 'value_error.missing'
    #   }]
    # }

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/managers/"
    username = "Manager2"
    new_manager = {"username": username}

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Manager1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.post(url=url, json=new_manager, headers=headers)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 422
    assert "password" in res_json["detail"][0]["loc"]
    assert res_json["detail"][0]["msg"] == "field required"
    assert res_json["detail"][0]["type"] == "value_error.missing"


def test_post_same_manager_returns_400(client):

    # Input
    # {
    #   "username": "Manager2"
    #   "password": "password1"
    # }
    #
    # Expected output
    # {'detail': 'Username already registered'}

    # Set up
    session, api_url = client
    url_login = f"{api_url}/auth/login"
    url = f"{api_url}/managers/"
    username = "Manager2"
    new_manager = {"username": username, "password": "password1"}

    # Login
    res_login = session.post(
        url=url_login, data={"username": "Manager1", "password": "password123"}
    )
    data = res_login.json()
    headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}

    # Exercise
    res = session.post(url=url, json=new_manager, headers=headers)
    # Try to create the same worker again
    res = session.post(url=url, json=new_manager, headers=headers)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 400
    assert res_json["detail"] == "Username already registered"
