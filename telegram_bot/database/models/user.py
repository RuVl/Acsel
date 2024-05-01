from typing import Optional

from sqlalchemy import Column, Integer, BigInteger, String, Enum
from sqlalchemy.orm import Mapped

from database.enums import UserRights
from . import Base


class User(Base):
    """ Table of telegram core users """

    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)

    telegram_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)
    username: Mapped[Optional[str]] = Column(String(255), nullable=True)

    rights: Mapped[int] = Column(Enum(UserRights), nullable=False, default=UserRights.USER)
