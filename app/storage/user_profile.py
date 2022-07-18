from sqlalchemy import delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import schemas
from app import models


class DuplicateEmail(Exception):
    ...


class UserProfileNotFound(Exception):
    ...


class UserProfileDAL:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_user_profile(self, user_id: int) -> models.UserProfile:
        """
        Returns one user profile found by user_id. If not found raises `UserProfileNotFound`
        """
        try:
            result = await self._session.execute(
                select(models.UserProfile).where(models.UserProfile.user_id == user_id)
            )

            return result.scalar_one()
        except NoResultFound as exc:
            raise UserProfileNotFound() from exc

    async def create_user_profile(self, user_profile: schemas.UserProfileCreate) -> int:
        """
        Adds new user profile to storage. Raises `DuplicateEmail` on... duplicate emails
        """
        if user_profile.email and await self._get_user_profile_by_email(
            user_profile.email
        ):
            raise DuplicateEmail()

        db_user_profile = models.UserProfile(
            email=user_profile.email,
            name=user_profile.name,
            birth_date=user_profile.birth_date,
        )

        self._session.add(db_user_profile)
        await self._session.commit()

        await self._session.refresh(db_user_profile)

        return db_user_profile.user_id

    async def update_user_profile(
        self, user_id: int, changes: schemas.UserProfileUpdate
    ) -> None:
        """
        Updates models with provided changes. Raises `UserProfileNotFound` if profile not found
        Raises `DuplicateEmail` if user with same email already exists
        """
        user_profile = await self.get_user_profile(user_id)

        if changes.email and (
            profile := await self._get_user_profile_by_email(changes.email)
        ):
            if profile.user_id != user_id:
                raise DuplicateEmail()

        for attr, value in changes.dict(exclude_unset=True).items():
            setattr(user_profile, attr, value)

        await self._session.commit()

    async def delete_user_profile(self, user_id: int) -> None:
        """
        Deletes user_profile with provided id. Raises `UserProfileNotFound` if nothing to delete
        """
        result = await self._session.execute(
            delete(models.UserProfile).where(models.UserProfile.user_id == user_id)
        )
        if result.rowcount == 0:
            raise UserProfileNotFound()

        await self._session.commit()

    async def _get_user_profile_by_email(self, email: str) -> models.UserProfile | None:
        result = await self._session.execute(
            select(models.UserProfile).where(models.UserProfile.email == email)
        )

        return result.scalar_one_or_none()
