# HRMS Lite Backend

This is the backend for the HRMS Lite application, built with Django and Django Rest Framework.

## Tech Stack

- **Framework**: Django 3.2.25 (Downgraded for Djongo compatibility)
- **API**: Django Rest Framework (DRF)
- **Database**: MongoDB (via Djongo)
- **Server**: Gunicorn (Production), Django Dev Server (Development)

## Setup Instructions

1.  **Prerequisites**:
    - **MongoDB**: Ensure MongoDB is running locally on port 27017, or update `.env` with your connection string.
    - **Python 3.x**

2.  **Clone the repository** (if you haven't already).
3.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Patch Djongo**:
    Run the patch script to fix compatibility issues with Django 3.2 and sqlparse 0.4.4:
    ```bash
    python patch_djongo.py
    ```
6.  **Configure Environment**:
    Create a `.env` file in `backend/` directory if not present:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
7.  **Run the server**:
    ```bash
    python manage.py runserver
    ```

## API Documentation

### Employees

- `GET /api/employees/`: List all employees.
- `POST /api/employees/`: Add a new employee.
- `DELETE /api/employees/<employee_id>/`: Delete an employee.

### Attendance

- `GET /api/attendance/`: List all attendance.
- `POST /api/attendance/`: Mark attendance.
- `GET /api/attendance/?employee_id=<id>`: Filter by employee.

## Deployment

The project is configured for deployment with `Gunicorn` and `WhiteNoise`.
Run with Gunicorn:

```bash
gunicorn hrms_core.wsgi
```
