from app.api.api_v1.api import api_router


def test_api_router():
    paths = [o.path for o in api_router.routes]

    assert "/workers/" in paths
    assert "/workers/{worker_id}" in paths
    assert "/workers/{worker_id}/shifts/" in paths
    assert "/workers/{worker_id}/shifts/{shift_id}" in paths
    assert "/managers/" in paths
    assert "/managers/{manager_id}" in paths
    assert "/shifts/" in paths
    assert "/shifts/{shift_id}" in paths
    assert "/auth/login" in paths
    assert "/auth/me" in paths
