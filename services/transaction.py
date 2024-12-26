from sqlalchemy.orm import Session
from models.transaction import Transaction
from schemas.transaction import TransactionCreate, TransactionUpdate
import datetime

def create_transaction(db: Session, transaction: TransactionCreate, user: int):
    db_transaction = Transaction(
        user_id=user,
        amount=transaction.amount,
        category=transaction.category,
        description=transaction.description,
        date=datetime.datetime.now(),
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(Transaction).filter(Transaction.user_id == user_id).offset(skip).limit(limit).all()

def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not db_transaction:
        return None
    for key, value in transaction.dict(exclude_unset=True).items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction
