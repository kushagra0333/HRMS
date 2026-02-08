# HRMS

This is a Human Resource Management System (HRMS) built with Django (Backend) and React (Frontend).

## Prerequisites

- Python 3.12+
- Node.js 18+
- MongoDB

## Setup Instructions

### Backend

1.  Navigate to the `backend` directory:

    ```bash
    cd backend
    ```

2.  Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    (Note: `pymongo[srv]` is included for MongoDB Atlas support).

4.  Set up environment variables:
    - Create a `.env` file in `backend/` or ensure `hrms_core/settings.py` has the correct `MONGODB_URL`.
    - Example `.env`:
      ```
      MONGODB_URL=mongodb://localhost:27017/hrms_db
      SECRET_KEY=your_secret_key
      DEBUG=True
      ```

5.  Apply migrations:

    ```bash
    python manage.py migrate
    ```

6.  Run the server:
    ```bash
    python manage.py runserver
    ```
    The backend will run at `http://127.0.0.1:8000/`.

### Frontend

1.  Navigate to the `frontend` directory:

    ```bash
    cd frontend
    ```

2.  Install dependencies:

    ```bash
    npm install
    ```

3.  Start the development server:
    ```bash
    npm start
    ```
    The frontend will run at `http://localhost:3000/`.

## Deployment

To deploy separately:

- **Backend:** accurate Python environment and `gunicorn` (e.g., on Render, Heroku).
- **Frontend:** Build the static files using `npm run build` and serve them (e.g., on Vercel, Netlify).
