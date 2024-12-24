from fastapi import FastAPI
from database import Base, engine
from routes import auth, transaction

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(transaction.router, prefix="/transactions", tags=["Transactions"])
