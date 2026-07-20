# Service Manager API

A FastAPI-based backend application for managing application migration data, user access, file uploads, and audit logging. The system supports Role-Based Access Control (RBAC), asynchronous CSV/Excel processing using Celery, and stores application metadata for reporting and visualization.

---

# Features

- User Authentication (JWT)
- Role-Based Access Control (RBAC)
- User Management
- File Upload (CSV/XLS/XLSX)
- Background File Processing with Celery
- Application Management
- Application Owner Management
- Migration Details
- Security Details
- Metadata Management
- Remarks Management
- Cloud Mapping
- Audit Logging
- Email Notifications
- Pagination
- Search & Filtering
- PostgreSQL Database
- Alembic Database Migrations

---

# Technology Stack

| Technology | Version |
|------------|----------|
| Python | 3.12+ |
| FastAPI | Latest |
| SQLAlchemy | 2.x |
| PostgreSQL | Latest |
| Alembic | Latest |
| Celery | Latest |
| Redis | Latest |
| Pandas | Latest |
| OpenPyXL | Latest |
| JWT | python-jose |
| Pydantic | v2 |

---

# Project Structure

```
app/
│
├── api/
│   └── endpoints/
│
├── core/
│
├── database/
│
├── models/
│
├── repositories/
│
├── schemas/
│
├── services/
│
├── tasks/
│
├── utils/
│
├── dependencies/
│
├── middleware/
│
└── main.py
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd servicemanager
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Configure Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/service_manager

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REDIS_URL=redis://localhost:6379/0

SMTP_SERVER=smtp.example.com

SMTP_PORT=587

SMTP_USERNAME=your_email@example.com

SMTP_PASSWORD=your_password

FROM_EMAIL=your_email@example.com
```

---

# Database Migration

Create migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

Apply migrations

```bash
alembic upgrade head
```

---

# Run FastAPI

```bash
uvicorn app.main:app --reload
```

API Documentation

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Run Redis

Example

```bash
redis-server
```

---

# Run Celery Worker

```bash
celery -A app.celery_app.celery worker --loglevel=info
```

---

# Authentication

The application uses JWT Authentication.

### Login

```
POST /auth/login
```

Returns

- Access Token
- Refresh Token

Include the access token in all protected requests.

```
Authorization: Bearer <token>
```

---

# Roles

- Admin
- Manager
- User

Permissions are enforced using RBAC.

---

# File Upload

Supported formats

- CSV
- XLS
- XLSX

Each uploaded file is

- Stored on disk
- Recorded in the database
- Processed asynchronously using Celery
- Parsed into application records
- Linked to cloud mappings
- Logged in Audit Logs

---

# Background Processing

After upload

1. File is saved
2. Upload record created
3. Celery task is queued
4. File is processed
5. Data is inserted/updated
6. Upload status updated

---

# Data Processed

Each application may include

- Application Details
- Owners
- Migration Details
- Security Information
- Metadata
- Remarks
- Cloud Mapping

---

# Audit Logs

The system records important activities including

- User Login
- User Creation
- User Update
- User Deletion
- File Upload
- File Deletion
- Record Updates

Each audit entry contains

- User
- Action
- Module
- Description
- Resource ID
- Previous Values
- New Values
- Timestamp

---

# Email Notifications

Celery sends emails for

- Welcome Email
- Password Reset (if enabled)

---

# Main Modules

- Authentication
- Users
- Roles
- Uploads
- Applications
- Migration
- Security
- Metadata
- Owners
- Remarks
- Cloud
- Audit Logs

---

# Error Handling

The API returns standard HTTP responses.

Example

```json
{
    "detail": "Resource not found"
}
```

Validation errors

```json
{
    "detail": [
        {
            "loc": [],
            "msg": "",
            "type": ""
        }
    ]
}
```

---

# API Documentation

Swagger

```
/docs
```

ReDoc

```
/redoc
```

---

# Development Commands

Run server

```bash
uvicorn app.main:app --reload
```

Run Celery

```bash
celery -A app.celery_app.celery worker --loglevel=info
```

Create migration

```bash
alembic revision --autogenerate -m "message"
```

Apply migration

```bash
alembic upgrade head
```

Rollback migration

```bash
alembic downgrade -1
```

---

# Future Enhancements

- Dashboard & Analytics
- Scheduled Reports
- Email Templates
- Multi-file Upload Progress
- File Versioning
- Soft Delete
- Docker Deployment
- Kubernetes Deployment

---

# License

This project is intended for internal organizational use.

---

# Author

Service Manager Development Team