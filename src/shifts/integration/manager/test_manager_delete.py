def test_delete_manager_deletes_manager(client):

    # Expected output
    # {
    #     "username": "Manager1",
    #     "id": 2,
    # }

    # Set up
    session, api_url = client
    url = f"{api_url}/managers/2"

    # Exercise
    res = session.delete(url=url)

    # Verify
    assert res.status_code == 200
    assert res.text == "2"


def test_delete_non_existent_manager_returns_404(client):

    # Expected output
    # {'detail': 'Manager not found'}

    # Set up
    session, api_url = client
    url = f"{api_url}/managers/1"

    # Exercise
    res = session.delete(url=url)

    # Verify
    res_json = res.json()
    print(res_json)
    assert res.status_code == 404
    assert res_json["detail"] == "Manager not found"
