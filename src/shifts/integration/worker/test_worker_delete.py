def test_delete_worker_deletes_worker(client):

    # Expected output
    # {
    #     "username": "Worker1",
    #     "id": 1,
    # }

    # Set up
    session, api_url = client
    url = f"{api_url}/workers/1"

    # Exercise
    res = session.delete(url=url)

    # Verify
    assert res.status_code == 200
    assert res.text == "1"


def test_delete_non_existent_worker_returns_404(client):

    # Expected output
    # {'detail': 'Worker not found'}

    # Set up
    session, api_url = client
    url = f"{api_url}/workers/2"

    # Exercise
    res = session.delete(url=url)

    # Verify
    res_json = res.json()
    print(res_json)
    assert res.status_code == 404
    assert res_json["detail"] == "Worker not found"
