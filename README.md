# 🚀 Backend Foundation

A production-ready Backend API built with **FastAPI**, **PostgreSQL**, **Redis**, **Celery**, and **Docker**.

This project demonstrates authentication, background jobs, REST APIs, logging, testing, and production-ready backend architecture.

---

# ✨ Features

## Authentication

- JWT Authentication
- User Registration
- Login
- Password Hashing (bcrypt)
- OTP Verification
- Email Verification
- Role-Based Authorization

## Posts

- Create Post
- Read Posts
- Update Post
- Delete Post
- Pagination
- Search
- Sorting

## Comments

- Add Comment
- Update Comment
- Delete Comment

## Likes

- Like Post
- Unlike Post

## Bookmarks

- Bookmark Post
- Remove Bookmark
- View My Bookmarks

## Background Tasks

- Celery
- Redis
- Email Queue

## Production Features

- Docker
- Docker Compose
- PostgreSQL
- SQLAlchemy ORM
- Alembic Migrations
- Logging
- Exception Handling
- Middleware
- Health Check
- Pytest

---

# 🛠 Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- Celery
- Docker
- JWT
- Pydantic
- Pytest

---

# 📂 Project Structure

```
backend-foundation/

├── app/
│   ├── api/
│   ├── auth/
│   ├── celery/
│   ├── config/
│   ├── database/
│   ├── email/
│   ├── exceptions/
│   ├── middleware/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   └── utils/
│
├── alembic/
├── tests/
├── uploads/
├── logs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── alembic.ini
├── main.py
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/hiteshkhairnar/backend-foundation.git
```

Go to project

```bash
cd backend-foundation
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🐳 Docker

Build containers

```bash
docker compose up --build
```

Run

```bash
docker compose up
```

Stop

```bash
docker compose down
```

---

# 🧪 Run Tests

```bash
pytest tests/
```

---

# 📖 API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# ❤️ Built With

- FastAPI
- PostgreSQL
- Docker
- Redis
- Celery