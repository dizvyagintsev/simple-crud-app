import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.storage.user_profile import UserProfileDAL


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="db_session")
async def fixture_db_session():
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture()
async def user_profile_dal(db_session):
    yield UserProfileDAL(db_session)


@pytest_asyncio.fixture(autouse=True)
async def truncate_user_profile_table(db_session: AsyncSession):
    await db_session.execute("truncate table user_profiles")
