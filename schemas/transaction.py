from pydantic import BaseModel
from datetime import datetime

class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str | None = None
    # date: datetime | None = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
