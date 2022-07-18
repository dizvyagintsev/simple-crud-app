import datetime

import pytest

from app.schemas import UserProfileCreate, UserProfileUpdate
from app.storage.user_profile import UserProfileDAL, DuplicateEmail, UserProfileNotFound


@pytest.mark.asyncio
async def test_create_user_profile(user_profile_dal: UserProfileDAL):
    user_id = await user_profile_dal.create_user_profile(
        UserProfileCreate(
            name="Denis Zvyagintsev",
            email="dizvyagintsev@gmail.com",
            birth_date=datetime.date(2000, 4, 7),
        )
    )

    profile = await user_profile_dal.get_user_profile(user_id)

    assert profile.user_id == user_id
    assert profile.name == "Denis Zvyagintsev"
    assert profile.email == "dizvyagintsev@gmail.com"
    assert profile.birth_date == datetime.date(2000, 4, 7)
    assert profile.is_banned is False


@pytest.mark.asyncio
async def test_create_user_profile_duplicate_emails(user_profile_dal: UserProfileDAL):
    await user_profile_dal.create_user_profile(
        UserProfileCreate(
            name="Denis Zvyagintsev",
            email="dizvyagintsev@gmail.com",
            birth_date=datetime.date(2000, 4, 7),
        )
    )

    with pytest.raises(DuplicateEmail):
        await user_profile_dal.create_user_profile(
            UserProfileCreate(
                name="Denis Zvyagintsev",
                email="dizvyagintsev@gmail.com",
                birth_date=datetime.date(2000, 4, 7),
            )
        )


@pytest.mark.asyncio
async def test_get_user_profile_not_found(user_profile_dal: UserProfileDAL):
    with pytest.raises(UserProfileNotFound):
        await user_profile_dal.get_user_profile(1)


@pytest.mark.asyncio
async def test_update_user_profile(user_profile_dal: UserProfileDAL):
    user_id = await user_profile_dal.create_user_profile(
        UserProfileCreate(
            name="Denis Zvyagintsev",
            email="dizvyagintsev@gmail.com",
            birth_date=datetime.date(2000, 4, 7),
        )
    )
    await user_profile_dal.update_user_profile(
        user_id=user_id,
        changes=UserProfileUpdate(
            name="Zvenis Dygintsev",
            email="dizvyagintsev@gmail.com",
            birth_date=datetime.date(2000, 7, 4),
        ),
    )

    profile = await user_profile_dal.get_user_profile(user_id)

    assert profile.user_id == user_id
    assert profile.name == "Zvenis Dygintsev"
    assert profile.email == "dizvyagintsev@gmail.com"
    assert profile.birth_date == datetime.date(2000, 7, 4)
    assert profile.is_banned is False


@pytest.mark.asyncio
async def test_update_user_profile_duplicate_email(user_profile_dal: UserProfileDAL):
    await user_profile_dal.create_user_profile(
        UserProfileCreate(
            name="Denis Zvyagintsev",
            email="dizvyagintsev@gmail.com",
            birth_date=datetime.date(2000, 4, 7),
        )
    )
    user_id = await user_profile_dal.create_user_profile(
        UserProfileCreate(
            name="Zvenis Dygintsev",
            email="zvdgntsv@gmail.com",
            birth_date=datetime.date(2000, 4, 7),
        )
    )

    with pytest.raises(DuplicateEmail):
        await user_profile_dal.update_user_profile(
            user_id=user_id,
            changes=UserProfileUpdate(email="dizvyagintsev@gmail.com"),
        )


@pytest.mark.asyncio
async def test_update_user_profile_not_found(user_profile_dal: UserProfileDAL):
    with pytest.raises(UserProfileNotFound):
        await user_profile_dal.update_user_profile(
            user_id=1,
            changes=UserProfileUpdate(email="dizvyagintsev@gmail.com"),
        )


@pytest.mark.asyncio
async def test_delete_user_profile(user_profile_dal: UserProfileDAL):
    user_id = await user_profile_dal.create_user_profile(
        UserProfileCreate(
            name="Denis Zvyagintsev",
            email="dizvyagintsev@gmail.com",
            birth_date=datetime.date(2000, 4, 7),
        )
    )
    await user_profile_dal.delete_user_profile(user_id)

    with pytest.raises(UserProfileNotFound):
        await user_profile_dal.get_user_profile(user_id)


@pytest.mark.asyncio
async def test_delete_user_profile_not_found(user_profile_dal: UserProfileDAL):
    with pytest.raises(UserProfileNotFound):
        await user_profile_dal.delete_user_profile(1)
