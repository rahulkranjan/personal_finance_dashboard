
# Personal Finance Tracker API

## Overview

The **Personal Finance Tracker API** is a robust backend system developed with **FastAPI** to help users manage their finances effectively. This API provides functionalities for tracking expenses, managing income, creating budgets, and generating reports.

---

## Features

- **User Authentication**:
  - Secure user registration and login using OAuth2 with password hashing.
  - Session management with JWT tokens and cookie-based authentication.
- **Expense and Income Tracking**:
  - Add, update, and delete transactions.
  - Categorize expenses and incomes for better tracking.
- **Secure and Scalable**:
  - Built with industry-standard security practices.
  - Modular design for easy scalability.

---

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Authentication**:  JWT
- **Deployment**: Docker, Gunicorn, Nginx
- **Testing**: Pytest

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- [Docker](https://www.docker.com/) (optional for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/personal_finance_dashboard.git
   cd personal_finance_dashboard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the root directory and define the following variables:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/finance_db
   SECRET_KEY=your_secret_key
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. Initialize the database:
   ```bash
   alembic upgrade head
   ```

6. Start the development server:
   ```bash
   uvicorn main:app --reload
   ```

   The API will be accessible at `http://127.0.0.1:8000`.

---

## API Endpoints

### Authentication
- `POST /auth/signup`: Register a new user.
- `POST /auth/login`: Login and obtain access tokens.
- `POST /auth/logout`: Logout user and invalidate tokens.

### Transactions
- `GET /transactions/`: List all transactions.
- `POST /transactions/`: Create a new transaction.
- `PUT /transactions/{id}`: Update a transaction.
- `DELETE /transactions/{id}`: Delete a transaction.

---

## Testing

Run the test suite using Pytest:
```bash
pytest
```

---

## Deployment

1. Build Docker image:
   ```bash
   docker build -t personal_finance_dashboard .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env personal_finance_dashboard
   ```
