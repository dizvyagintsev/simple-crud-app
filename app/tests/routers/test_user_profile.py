import datetime
from unittest.mock import AsyncMock

from fastapi import status
from fastapi.testclient import TestClient

from app import schemas, models
from app.dependencies import get_user_profile_dal
from app.main import app
from app.storage.user_profile import DuplicateEmail, UserProfileNotFound

mocked_user_profile_dal = AsyncMock()


def override_get_user_profile_dal():
    yield mocked_user_profile_dal


app.dependency_overrides[get_user_profile_dal] = override_get_user_profile_dal


def test_create_user_profile(client: TestClient):
    mocked_user_profile_dal.create_user_profile = AsyncMock(return_value=123456789)

    response = client.post(
        "/api/profile/", json={"name": "Denis Zvyagintsev", "birth_date": "2000-07-04"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"user_id": 123456789}

    mocked_user_profile_dal.create_user_profile.assert_awaited_once_with(
        schemas.UserProfileCreate(
            name="Denis Zvyagintsev", birth_date=datetime.date(2000, 7, 4)
        )
    )


def test_create_user_profile_duplicate_email(client: TestClient):
    mocked_user_profile_dal.create_user_profile = AsyncMock(side_effect=DuplicateEmail)

    response = client.post(
        "/api/profile/", json={"name": "Denis Zvyagintsev", "birth_date": "2000-07-04"}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Email already registered"}


def test_get_user_profile(client: TestClient):
    mocked_user_profile_dal.get_user_profile = AsyncMock(
        return_value=models.UserProfile(
            name="Denis Zvyagintsev",
            birth_date=datetime.date(2000, 7, 4),
            user_id=123456789,
            is_banned=False,
        )
    )

    response = client.get("/api/profile/123456789")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": "Denis Zvyagintsev",
        "birth_date": "2000-07-04",
        "user_id": 123456789,
        "is_banned": False,
    }

    mocked_user_profile_dal.get_user_profile.assert_awaited_once_with(123456789)


def test_get_user_profile_not_found(client: TestClient):
    mocked_user_profile_dal.get_user_profile = AsyncMock(
        side_effect=UserProfileNotFound
    )

    response = client.get("/api/profile/123456789")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User profile not found"}


def test_update_user_profile(client: TestClient):
    mocked_user_profile_dal.update_user_profile = AsyncMock()

    response = client.put("/api/profile/123456789", json={"is_banned": True})

    assert response.status_code == status.HTTP_204_NO_CONTENT

    mocked_user_profile_dal.update_user_profile.assert_awaited_once_with(
        123456789,
        schemas.UserProfileUpdate(is_banned=True),
    )


def test_update_user_profile_not_found(client: TestClient):
    mocked_user_profile_dal.update_user_profile = AsyncMock(
        side_effect=UserProfileNotFound
    )

    response = client.put("/api/profile/123456789", json={"is_banned": True})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User profile not found"}


def test_update_user_profile_duplicate_email(client: TestClient):
    mocked_user_profile_dal.update_user_profile = AsyncMock(side_effect=DuplicateEmail)

    response = client.put("/api/profile/123456789", json={"is_banned": True})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Email already registered"}


def test_delete_user_profile(client: TestClient):
    mocked_user_profile_dal.delete_user_profile = AsyncMock()

    response = client.delete("/api/profile/123456789")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    mocked_user_profile_dal.delete_user_profile.assert_awaited_once_with(123456789)


def test_delete_user_profile_not_found(client: TestClient):
    mocked_user_profile_dal.delete_user_profile = AsyncMock(
        side_effect=UserProfileNotFound
    )

    response = client.delete("/api/profile/123456789")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User profile not found"}
