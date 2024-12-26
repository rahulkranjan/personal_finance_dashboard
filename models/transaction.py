from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum


class TransactionCategory(enum.Enum):
    expense = "expense"
    income = "income"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    category = Column(Enum(TransactionCategory), nullable=False)
    description = Column(String)
    date = Column(DateTime, default=datetime.now)

    user = relationship("User")