import datetime

from pydantic import BaseModel


class UserProfileCreate(BaseModel):
    email: str | None
    name: str
    birth_date: datetime.date


class UserProfile(UserProfileCreate):
    user_id: int
    is_banned: bool

    class Config:
        orm_mode = True


class UserProfileUpdate(UserProfileCreate):
    name: str | None
    birth_date: datetime.date | None
    is_banned: bool | None


class UserProfileCreateOut(BaseModel):
    user_id: int
