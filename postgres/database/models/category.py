from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, inspect
from sqlalchemy.orm import Mapped, relationship

from database.models import Base

if TYPE_CHECKING:
    from database.models import Product


class Category(Base):
    """ Table of product categories """

    __tablename__ = 'categories'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(255), nullable=False, unique=True)

    total_products: Mapped[int] = Column(Integer, nullable=False, default=0)
    products: Mapped[list['Product']] = relationship('Product', back_populates='category')

    def __repr__(self) -> str:
        insp = inspect(self)
        products = [] if 'products' in insp.unloaded else self.products
        return f'<Category ({self.id}) {self.name} - {self.total_products} pcs : {products}>'

    def __str__(self) -> str:
        return f'{self.name} ({self.total_products})'
