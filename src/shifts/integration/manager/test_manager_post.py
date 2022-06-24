def test_post_manager_creates_manager(client):

    # Input
    # {
    #   "username": "Manager2"
    # }
    #
    # Expected output
    # {
    #     "username": "Manager2",
    #     "id": 3,
    # }

    # Set up
    session, api_url = client
    url = f"{api_url}/managers/"
    username = "Manager2"
    data = {"username": username}

    # Exercise
    res = session.post(url=url, json=data)

    # Verify
    res_json = res.json()
    # caplog.info(res_json)
    assert res.status_code == 201
    assert res_json["id"] == 3
    assert res_json["username"] == username


def test_post_same_manager_returns_400(client):

    # Input
    # {
    #   "username": "Manager2"
    # }
    #
    # Expected output
    # {'detail': 'Username already registered'}

    # Set up
    session, api_url = client
    url = f"{api_url}/managers/"
    username = "Manager2"
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
