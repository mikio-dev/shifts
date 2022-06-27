import pytest
from app.main import root


@pytest.mark.asyncio
async def test_root():
    message = await root()
    assert message == {"message": "ok"}
