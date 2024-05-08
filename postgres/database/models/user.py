from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, Integer, BigInteger, String, Enum
from sqlalchemy.orm import Mapped, relationship

from database.enums import UserRights
from database.models import Base

if TYPE_CHECKING:
    from database.models import Transaction


class User(Base):
    """ Table of telegram users """

    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)

    telegram_id: Mapped[int] = Column(BigInteger, unique=True, nullable=False)
    username: Mapped[Optional[str]] = Column(String(255), nullable=True)

    rights: Mapped[int] = Column(Enum(UserRights), nullable=False, default=UserRights.USER)

    transactions: Mapped['Transaction'] = relationship('Transaction', back_populates='user')
