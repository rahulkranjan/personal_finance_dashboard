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
import httpx
from fastapi.responses import StreamingResponse
import csv
import io
from datetime import datetime


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
            func.count(Transaction.id).label("total_transactions"), 
            func.sum(
                case(
                    (Transaction.category == TransactionCategory.income, Transaction.amount), 
                    else_=0,
                )
            ).label("total_income"),
            func.sum(
                case(
                    (Transaction.category == TransactionCategory.expense, Transaction.amount),
                    else_=0,
                )
            ).label("total_expense"),
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


@router.get("/exchange-rate")
async def get_exchange_rate():

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'http://api.exchangeratesapi.io/v1/latest',
                params={
                    "access_key": 'f118b0bd729d80ee94fbe0505f058214',
                    "symbols": "USD,AUD,CAD,PLN,MXN",
                },
            )
            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail="Error fetching exchange rate data")
            data = response.json()
            return {'result': data}

    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching exchange rates: {exc}")



@router.get("/report", response_class=StreamingResponse)
async def generate_csv_report(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        transactions = db.query(Transaction).filter(user_id = current_user).all()

        if not transactions:
            raise HTTPException(status_code=404, detail="No transactions found")

        buffer = io.StringIO()
        writer = csv.writer(buffer)

        writer.writerow(["Date", "Description", "Category", "Amount"])

        for transaction in transactions:
            writer.writerow([
                transaction.date.strftime("%Y-%m-%d"),
                transaction.description,
                transaction.category,
                transaction.amount,
            ])

        buffer.seek(0)

        filename = f"expenses_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the CSV: {e}")