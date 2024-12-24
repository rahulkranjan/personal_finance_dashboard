from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.transaction import (
    get_transaction,
    get_transactions,
    create_transaction,
    update_transaction,
    delete_transaction,
)
from schemas.transaction import TransactionCreate, TransactionUpdate, TransactionOut
from utils import get_current_user
from models.user import User

router = APIRouter()

@router.get("/", response_model=list[TransactionOut])
def list_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    transactions = get_transactions(db, user_id=current_user.id, skip=skip, limit=limit)
    return transactions

@router.get("/{transaction_id}", response_model=TransactionOut)
def read_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends()):
    transaction = get_transaction(db, transaction_id)
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction

@router.post("/add-transaction/", response_model=TransactionOut, status_code=status.HTTP_201_CREATED)
def create_new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_transaction(db, transaction, user_id=current_user.id)

@router.put("/{transaction_id}", response_model=TransactionOut)
def update_existing_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db), current_user: User = Depends()):
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction or db_transaction.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return update_transaction(db, transaction_id, transaction)

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends()):
    db_transaction = get_transaction(db, transaction_id)
    if not db_transaction or db_transaction.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    delete_transaction(db, transaction_id)
    return {"message": "Transaction deleted successfully"}
