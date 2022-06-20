from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

from app.api import deps
from app.main import app
from app.models.manager import Manager
from app.models.shift import Shift
from app.models.worker import Worker
from app.models.worker_shift import WorkerShift


async def mock_db_no_result():
    """
    Mock db session that simulates no record is returned from the query
    """
    mock = MagicMock()
    mock.query().filter().first.return_value = None

    return mock


async def mock_db_manager():
    """
    Mock db session that simulates the following query results:
    - The offset().limit().all() query returns 5 manager records.
    - The filter().first() query returns one manager record.
    """
    mock = MagicMock()

    managers = []
    managers.append(Manager(id=1, username="Manager1"))
    managers.append(Manager(id=2, username="Manager2"))
    managers.append(Manager(id=3, username="Manager3"))
    managers.append(Manager(id=4, username="Manager4"))
    managers.append(Manager(id=5, username="Manager5"))

    mock.query().offset().limit().all.return_value = managers
    mock.query().filter().first.return_value = managers[0]

    return mock


async def mock_db_worker():
    """
    Mock db session that simulates the following query results:
    - The offset().limit().all() query returns 5 worker records.
    - The filter().first() query returns one worker record.
    """
    mock = MagicMock()

    workers = []
    workers.append(Worker(id=1, username="Worker1"))
    workers.append(Worker(id=2, username="Worker2"))
    workers.append(Worker(id=3, username="Worker3"))
    workers.append(Worker(id=4, username="Worker4"))
    workers.append(Worker(id=5, username="Worker5"))

    mock.query().offset().limit().all.return_value = workers
    mock.query().filter().first.return_value = workers[0]

    return mock


async def mock_db_shift():
    """
    Mock db session that simulates the following query results:
    - The offset().limit().all() query returns 5 shift records.
    - The filter().first() query returns one shift record.
    """
    mock = MagicMock()

    shifts = []
    shifts.append(Shift(id=1, shift_date="2022-01-01", shift_slot=1))
    shifts.append(Shift(id=2, shift_date="2022-01-02", shift_slot=2))
    shifts.append(Shift(id=3, shift_date="2022-01-03", shift_slot=3))
    shifts.append(Shift(id=4, shift_date="2022-01-04", shift_slot=1))
    shifts.append(Shift(id=5, shift_date="2022-01-05", shift_slot=2))

    mock.query().offset().limit().all.return_value = shifts
    mock.query().filter().first.return_value = shifts[0]

    return mock


async def mock_db_worker_shift():
    """
    Mock db session that simulates the following query results:
    - The first filter().first() query returns a worker record.
    - The second filter().first() query returns a shift record.
    - The third filter().first() query returns no record.
    - The join().join().filter().first() query returns no record.

    """
    mock = MagicMock()

    worker_shift = (
        Worker(id=1, username="Worker1"),
        Shift(id=1, shift_date="2022-01-01", shift_slot=1),
        None,
    )
    mock.query().filter().first.side_effect = worker_shift
    mock.query().join().join().filter().first.return_value = None

    return mock


async def mock_db_worker_shift_found():
    """
    Mock db session that simulate the following query results:
    - The first filter().first() query returns a worker record.
    - The second filter().first() query returns a shift record.
    - The third filter().first() query returns a worker_shift record.
    - The fourth filter().first() query returns a worker_shift record.
    - The third join().join().filter().first() query returns a worker_shift record.
    """
    mock = MagicMock()

    worker_shift = (
        Worker(id=1, username="Worker1"),
        Shift(id=1, shift_date="2022-01-01", shift_slot=1),
        WorkerShift(worker_id=1, shift_id=1, shift_date="2022-01-01"),
        WorkerShift(worker_id=1, shift_id=1, shift_date="2022-01-01"),
    )
    mock.query().filter().first.side_effect = worker_shift
    mock.query().join().join().filter().first.return_value = WorkerShift(
        worker_id=1, shift_id=1, shift_date="2022-01-01"
    )

    return mock


async def mock_db_worker_shift_integrity_error():
    """
    Mock db session that simulates the following query results:
    - The first filter().first() query returns a worker record.
    - The second filter().first() query returns a shift record.
    - The third join().join().filter().first() query returns no record.
    - The insert raises IntegrityError.
    """
    mock = MagicMock()

    worker_shift = (
        Worker(id=1, username="Worker1"),
        Shift(id=1, shift_date="2022-01-01", shift_slot=1),
    )
    mock.query().filter().first.side_effect = worker_shift
    mock.query().join().join().filter().first.return_value = None
    mock.add.side_effect = IntegrityError("", "", "")

    return mock


@pytest.fixture
def no_result_client() -> Generator:
    """
    Test client fixture that replaces the dependent db session
    with the `mock_db_no_result` mock db session
    """
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_db] = mock_db_no_result
        yield client
        app.dependency_overrides = {}


@pytest.fixture
def manager_client() -> Generator:
    """
    Test client fixture that replaces the dependent db session
    with the `mock_db_manager` mock db session
    """
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_db] = mock_db_manager
        yield client
        app.dependency_overrides = {}


@pytest.fixture
def worker_client() -> Generator:
    """
    Test client fixture that replaces the dependent db session
    with the `mock_db_worker` mock db session
    """
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_db] = mock_db_worker
        yield client
        app.dependency_overrides = {}


@pytest.fixture
def shift_client() -> Generator:
    """
    Test client fixture that replaces the dependent db session
    with the `mock_db_shift` mock db session
    """
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_db] = mock_db_shift
        yield client
        app.dependency_overrides = {}


@pytest.fixture
def worker_shift_client() -> Generator:
    """
    Test client fixture that replaces the dependent db session
    with the `mock_db_worker_shift` mock db session
    """
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_db] = mock_db_worker_shift
        yield client
        app.dependency_overrides = {}


@pytest.fixture(
    params=[mock_db_worker_shift_found, mock_db_worker_shift_integrity_error]
)
def worker_shift_add_error_client(request) -> Generator:
    """
    Test client fixture that replaces the dependent db session
    with the parametrized mock db sessions:
    - `mock_db_worker_shift_found`
    - `mock_db_worker_shift_integrity_error`
    """
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_db] = request.param

        yield client
        app.dependency_overrides = {}


@pytest.fixture
def worker_shift_delete_client() -> Generator:
    """
    Test client fixture that replaces the dependent db session
    with the `mock_db_worker_shift_found` mock db session
    """
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_db] = mock_db_worker_shift_found
        yield client
        app.dependency_overrides = {}


@pytest.fixture(params=[mock_db_no_result, mock_db_worker_shift])
def worker_shift_delete_error_client(request) -> Generator:
    """
    Test client fixture that replaces the dependent db session
    with the parametrized mock db sessions:
    - `mock_db_no_result`
    - `mock_db_worker_shift`
    """
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_db] = request.param

        yield client
        app.dependency_overrides = {}
