from typing import TYPE_CHECKING

from sqlalchemy import Column, String, Integer, Text, Numeric, ForeignKey, inspect
from sqlalchemy.orm import Mapped, relationship

from database.models import Base, Category

if TYPE_CHECKING:
    from database.models import ProductFile


class Product(Base):
    """ Table of products """

    __tablename__ = 'products'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(255), nullable=False, unique=True)
    description: Mapped[str] = Column(Text)

    price: Mapped[float] = Column(Numeric, nullable=False)
    quantity: Mapped[int] = Column(Integer, nullable=False, default=0)
    files: Mapped[list['ProductFile']] = relationship('ProductFile', back_populates='product')

    category: Mapped['Category'] = relationship('Category', back_populates='products')
    category_id: Mapped[int] = Column(ForeignKey('categories.id'), nullable=False)

    def __repr__(self) -> str:
        insp = inspect(self)

        category_name = None if 'category' in insp.unloaded else self.category.name
        files = [] if 'files' in insp.unloaded else self.files

        return (f'<Product ({self.id}) {self.name} - {self.description} : '
                f'${self.price}, {self.quantity} pcs : {files}, '
                f'{self.category_id} - {category_name}>')

    def __str__(self) -> str:
        return f'{self.name} ({self.quantity})'
