def test_delete_shift_deletes_shift(client):

    # Expected output
    # {
    #     "username": "shift1",
    #     "id": 1,
    # }

    # Set up
    session, api_url = client
    url = f"{api_url}/shifts/1"

    # Exercise
    res = session.delete(url=url)

    # Verify
    assert res.status_code == 200
    assert res.text == "1"


def test_delete_non_existent_shift_returns_404(client):

    # Expected output
    # {'detail': 'Not Found'}

    # Set up
    session, api_url = client
    url = f"{api_url}/shift/100"

    # Exercise
    res = session.delete(url=url)

    # Verify
    res_json = res.json()
    print(res_json)
    assert res.status_code == 404
    assert res_json["detail"] == "Not Found"
