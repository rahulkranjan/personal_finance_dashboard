from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.transaction import Transaction, TransactionCategory
from schemas.transaction import TransactionData, TransactionCreate, TransactionUpdate
from services.transaction import (
    create_transaction,
    get_transaction,
    get_transactions,
    update_transaction,
    delete_transaction,
)
from utils import get_current_user
from sqlalchemy import func, case

router = APIRouter()

@router.post("/", response_model=TransactionData)
def create_new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_transaction(db, transaction, current_user)

# @router.get("/{transaction_id}", response_model=Transaction)
# def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
#     transaction = get_transaction(db, transaction_id)
#     if not transaction:
#         raise HTTPException(status_code=404, detail="Transaction not found")
#     return transaction

@router.get("/", response_model=list[TransactionData])
def read_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_transactions(db, current_user, skip, limit)


@router.put("/{transaction_id}", response_model=TransactionData)
def update_existing_transaction(
    transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)
):
    updated_transaction = update_transaction(db, transaction_id, transaction)
    if not updated_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return updated_transaction


@router.delete("/{transaction_id}", response_model=TransactionData)
def delete_existing_transaction(transaction_id: int, db: Session = Depends(get_db)):
    deleted_transaction = delete_transaction(db, transaction_id)
    if not deleted_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return deleted_transaction


@router.get("/summary", summary="Get transaction summary")
def get_transaction_summary(
        db: Session = Depends(get_db),
        current_user: dict = Depends(get_current_user)
    ):

    result = (
        db.query(
            func.count(Transaction.id).label("total_transactions"),  # Count transactions
            func.sum(
                case(
                    (Transaction.category == TransactionCategory.income, Transaction.amount),  # Positional `when`
                    else_=0,
                )
            ).label("total_income"),  # Total income
            func.sum(
                case(
                    (Transaction.category == TransactionCategory.expense, Transaction.amount),  # Positional `when`
                    else_=0,
                )
            ).label("total_expense"),  # Total expense
        )
        .filter(Transaction.user_id == current_user)
        .first()
    )

    if not result:
        raise HTTPException(status_code=404, detail="No transactions found")

    return {
        "total_transactions": int(result.total_transactions or 0),
        "total_income": int(result.total_income or 0),
        "total_expense": int(result.total_expense or 0),
    }