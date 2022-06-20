from app.core.config import settings


def test_api_v1_str():
    assert settings.API_V1_STR == "/api/v1"


def test_sqlalchemy_database_uri():
    assert (
        settings.SQLALCHEMY_DATABASE_URI
        == "postgresql://postgres:postgres@localhost:5432/shifts"
    )


def test_first_manager():
    assert settings.FIRST_MANAGER == "Manager1"


def test_first_worker():
    assert settings.FIRST_WORKER == "Worker1"
