import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
from models.user import User
from models.transaction import Transaction, TransactionCategory
from services.auth import get_password_hash, create_access_token
from datetime import datetime

# Configure test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixtures
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

# Helper functions
def create_test_user(db):
    password = get_password_hash("password123")
    user = User(username="testuser", email="testuser@example.com", password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Authentication Tests
def test_signup(client, test_db):
    response = client.post("/signup", json={"username": "newuser", "email": "newuser@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"

def test_login(client, test_db):
    create_test_user(test_db)
    response = client.post("/login", json={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert "message" in response.json()

def test_check_auth(client, test_db):
    user = create_test_user(test_db)
    token = create_access_token({"sub": user.username})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/check", cookies={"access_token": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "testuser"

def test_logout(client):
    response = client.post("/logout", cookies={"access_token": "Bearer fake_token"})
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"

# Transaction Tests
def test_create_transaction(client, test_db):
    user = create_test_user(test_db)
    token = create_access_token({"sub": user.username})
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "amount": 1000,
        "category": "income",
        "description": "Salary",
        "date": str(datetime.utcnow())
    }
    response = client.post("/transactions/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json()["description"] == "Salary"

def test_read_transactions(client, test_db):
    user = create_test_user(test_db)
    token = create_access_token({"sub": user.username})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/transactions/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_transaction(client, test_db):
    user = create_test_user(test_db)
    token = create_access_token({"sub": user.username})
    headers = {"Authorization": f"Bearer {token}"}

    # Create transaction
    transaction = Transaction(
        user_id=user.id,
        amount=100,
        category=TransactionCategory.expense,
        description="Groceries",
        date=datetime.utcnow(),
    )
    test_db.add(transaction)
    test_db.commit()
    test_db.refresh(transaction)

    # Update transaction
    update_data = {"amount": 200, "description": "Updated Groceries"}
    response = client.put(f"/transactions/{transaction.id}", json=update_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["amount"] == 200

def test_delete_transaction(client, test_db):
    user = create_test_user(test_db)
    token = create_access_token({"sub": user.username})
    headers = {"Authorization": f"Bearer {token}"}

    # Create transaction
    transaction = Transaction(
        user_id=user.id,
        amount=100,
        category=TransactionCategory.expense,
        description="Groceries",
        date=datetime.utcnow(),
    )
    test_db.add(transaction)
    test_db.commit()
    test_db.refresh(transaction)

    # Delete transaction
    response = client.delete(f"/transactions/{transaction.id}", headers=headers)
    assert response.status_code == 200

def test_transaction_summary(client, test_db):
    user = create_test_user(test_db)
    token = create_access_token({"sub": user.username})
    headers = {"Authorization": f"Bearer {token}"}

    # Add transactions
    transactions = [
        Transaction(
            user_id=user.id,
            amount=500,
            category=TransactionCategory.income,
            description="Bonus",
            date=datetime.utcnow(),
        ),
        Transaction(
            user_id=user.id,
            amount=200,
            category=TransactionCategory.expense,
            description="Utilities",
            date=datetime.utcnow(),
        ),
    ]
    test_db.add_all(transactions)
    test_db.commit()

    # Fetch summary
    response = client.get("/transactions/summary", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total_income"] == 500
    assert data["total_expense"] == 200

def test_exchange_rate(client):
    response = client.get("/transactions/exchange-rate")
    assert response.status_code == 200
    assert "result" in response.json()
