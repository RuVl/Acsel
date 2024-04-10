from sqlalchemy import Column, String, Integer, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from database.models import Base, Category


class Product(Base):
    """ Table of products """

    __tablename__ = 'products'

    id: Mapped[int] = Column(Integer, primary_key=True)

    name: Mapped[str] = Column(String(255), nullable=False, unique=True)
    description: Mapped[str] = Column(Text)

    price: Mapped[int] = Column(Numeric, nullable=False)
    quantity: Mapped[int] = Column(Integer, nullable=False, default=0)

    category: Mapped['Category'] = relationship('Category', back_populates='products')
    category_id: Mapped[int] = Column(ForeignKey('categories.id'), nullable=False)
