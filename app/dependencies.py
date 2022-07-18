from app.database import async_session
from app.storage.user_profile import UserProfileDAL


async def get_user_profile_dal():
    async with async_session() as session:
        yield UserProfileDAL(session)
