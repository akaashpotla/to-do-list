# DoIt - A To-Do List Application

A full stack to do list application with JWT authentication, built with FastAPI and React.

## Tech Stack:
**Backend:**
- FastAPI / Python
- SQLAlchemy (ORM)
- Alembic (migrations)
- Pydantic for validation
- Pytest for testing

**Frontend:**
- React
- React Router
- React Bootstrap

**Database:**
- PostgreSQL

**Authentication:**
- JWT authentication (httpOnly cookies)

Before you get started, make sure you have the following installed:
* Docker (https://www.docker.com/products/docker-desktop/)
* Python 3.11+ (https://www.python.org/downloads/)
* Node.js (https://nodejs.org/en/)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/akaashpotla/to-do-list.git
cd to-do-list
```

### 2. Start the database

```bash
docker compose up -d
```

This starts a PostgreSQL instance on port `5433`.

### 3. Set up the backend

```bash
python -m venv .venv
source .venv/bin/activate     # For Mac/Linux
.venv\Scripts\activate        # For Windows

pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://akaashpotla:apples@localhost:5433/todo_db
SECRET_KEY=your_secret_key_here
```

Run database migrations:

```bash
alembic upgrade head
```

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.
Interactive API docs at `http://localhost:8000/docs`.

### 4. Set up the frontend

```bash
cd client
npm install
npm start
```

## Running Tests

From the project root:

```bash
pytest
```


## Environment Variables

`DATABASE_URL` : PostgreSQL connection string

`SECRET_KEY` : Secret key used to sign JWT tokens
