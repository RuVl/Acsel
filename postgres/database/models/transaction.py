from sqlalchemy import Column, Integer, String, Enum, Numeric, ForeignKey, Sequence
from sqlalchemy.orm import Mapped, relationship

from database.enums import TransactionStatuses
from database.models import Base, ProductFile, User


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = Column(Integer, Sequence('transactions_id_seq'), primary_key=True)

    total_price: Mapped[float] = Column(Numeric, nullable=False)
    quantity: Mapped[int] = Column(Integer, nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='transactions')
    user_id: Mapped[int] = Column(ForeignKey('users.id'), nullable=False)

    files: Mapped[list['ProductFile']] = relationship('ProductFile', back_populates='transaction')

    # Plisio fields
    txn_id: Mapped[str] = Column(String, unique=True, nullable=False)
    status: Mapped[int] = Column(Enum(TransactionStatuses), nullable=False, default=TransactionStatuses.NONE)
    confirmations: Mapped[int] = Column(Integer)

    amount: Mapped[float] = Column(Numeric)
    currency: Mapped[str] = Column(String)

    source_amount: Mapped[float] = Column(Numeric)
    source_currency: Mapped[str] = Column(String)
    source_rate: Mapped[float] = Column(Numeric)

    comment: Mapped[str] = Column(String)

    invoice_commission: Mapped[float] = Column(Numeric)
    invoice_sum: Mapped[float] = Column(Numeric)
    invoice_total_sum: Mapped[float] = Column(Numeric)
