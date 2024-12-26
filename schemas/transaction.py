from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TransactionCategory(str, Enum):
    expense = "expense"
    income = "income"

class TransactionBase(BaseModel):
    amount: float
    category: TransactionCategory
    description: str | None = None
    date: datetime | None = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    amount: float | None = None
    category: TransactionCategory | None = None
    description: str | None = None

class TransactionData(TransactionBase):
    id: int
    # date: datetime

    class Config:
        from_attributes = True


