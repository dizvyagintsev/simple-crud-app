from sqlalchemy import Column, BigInteger, String, Date, Boolean

from app.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(40), nullable=True)
    name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=False)
    is_banned = Column(Boolean, default=False, nullable=False)
