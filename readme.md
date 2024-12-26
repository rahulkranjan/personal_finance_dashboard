
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
- **Budget Management**:
  - Set budgets for specific categories or time periods.
  - Alerts for budget overages.
- **Reporting**:
  - Generate insights on spending habits.
  - View summary reports for specific timeframes or categories.
- **Secure and Scalable**:
  - Built with industry-standard security practices.
  - Modular design for easy scalability.

---

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL (or any preferred RDBMS)
- **Authentication**: OAuth2, JWT
- **Deployment**: Docker, Gunicorn, Nginx (Optional)
- **Testing**: Pytest

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL or any preferred database
- [Docker](https://www.docker.com/) (optional for containerized deployment)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/personal-finance-tracker.git
   cd personal-finance-tracker
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

### Budgets
- `GET /budgets/`: List all budgets.
- `POST /budgets/`: Create a new budget.
- `PUT /budgets/{id}`: Update a budget.
- `DELETE /budgets/{id}`: Delete a budget.

### Reports
- `GET /reports/summary`: Get summary reports.
- `GET /reports/{category}`: Get reports by category.

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
   docker build -t personal-finance-tracker .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8000:8000 --env-file .env personal-finance-tracker
   ```

---

## Contributing

Contributions are welcome! Please follow the steps below:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add some feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
