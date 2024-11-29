from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pytest_asyncio import is_async_test
from sqlalchemy import delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import engine, init_db
from app.main import app
from app.models.item import Item
from app.tests.utils.utils import get_x_api_key_header


@pytest_asyncio.fixture(loop_scope="session", scope="session", autouse=True)
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture
def x_api_key_header() -> dict[str, str]:
    """Fixture to provide an X-API-Key header."""
    return get_x_api_key_header()


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None, None]:
    async with AsyncSession(engine) as session:
        await init_db()
        yield session
        statement = delete(Item)
        await session.exec(statement)  # type: ignore[call-overload]
        await session.commit()
        # await restart_db()
