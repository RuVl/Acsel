from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from database.models import Base

if TYPE_CHECKING:
    from database.models import Product


class Category(Base):
    """ Table of product categories """

    __tablename__ = 'categories'

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(255), nullable=False)

    total_products: Mapped[int] = Column(Integer, nullable=False, default=0)
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')
