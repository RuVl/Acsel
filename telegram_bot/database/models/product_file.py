from sqlalchemy import Column, Integer, ForeignKey, inspect, String
from sqlalchemy.orm import Mapped, relationship

from . import Base, Product


class ProductFile(Base):
    __tablename__ = 'product_files'

    id: Mapped[int] = Column(Integer, primary_key=True)

    path: Mapped[str] = Column(String(255), nullable=False)

    product: Mapped['Product'] = relationship('Product', back_populates='files')
    product_id: Mapped[int] = Column(ForeignKey('products.id'), nullable=False)

    def __repr__(self) -> str:
        insp = inspect(self)
        product_name = None if 'product' in insp.unloaded else self.product.name
        return f'<File ({self.id}) {self.path}, {self.product_id} - {product_name}>'
