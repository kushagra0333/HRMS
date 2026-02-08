# HRMS - Human Resource Management System

A comprehensive and modern Human Resource Management System (HRMS) designed to streamline employee management, attendance tracking, and leave management processes. Built with a robust **Django** backend and a responsive **React** frontend, this application offers a seamless experience for both administrators and employees.

## 🚀 Key Features

### 🔐 Authentication & Security

- **Secure Login/Register**: JWT-based authentication using `djangorestframework-simplejwt`.
- **Role-Based Access**: Separation of concerns between Admin and Employee roles.
- **Protected Routes**: Frontend routes secured ensuring only authenticated users can access sensitive data.

### 👥 Employee Management

- **Centralized Database**: Store and manage comprehensive employee records.
- **CRUD Operations**: Admins can easily Add, View, and Delete employee profiles.
- **Search Functionality**: Quickly find employees by name or ID.

### 📅 Attendance Tracking

- **Daily Marking**: Simple interface for marking daily attendance (Present/Absent).
- **History View**: Employees can view their own attendance history.
- **Admin Overview**: Admins get a daily summary of workforce presence.

### 🏖️ Leave Management

- **Digital Applications**: Employees can apply for leaves with reasons and dates.
- **Status Tracking**: Real-time updates on leave status (Pending ⏳, Approved ✅, Rejected ❌).
- **Approval Workflow**: Admins can review pending leave requests and approve/reject them instantly.

### 📊 Interactive Dashboard

- **Real-time Stats**: Instant view of Total Employees, Present Today, Pending Leaves, and more.
- **Personalized View**: Employees see their own stats, while Admins see organization-wide metrics.

### 📱 Fully Responsive Design

- **Mobile-First Approach**: Optimized for all screen sizes (Mobile, Tablet, Desktop).
- **Collapsible Sidebar**: Smooth navigation on smaller screens with a mobile-friendly menu.
- **Adaptive Tables**: Data tables that scroll horizontally on mobile devices without breaking layout.

---

## 🛠️ Tech Stack

### Frontend

- **React.js**: Component-based UI library.
- **Tailwind CSS**: Utility-first CSS framework for rapid and responsive styling.
- **Lucide React**: Beautiful and consistent icons.
- **Axios**: Promise-based HTTP client for API requests.
- **React Router DOM**: Declarative routing for Single Page Applications (SPA).

### Backend

- **Django**: High-level Python web framework.
- **Django REST Framework (DRF)**: Powerful toolkit for building Web APIs.
- **MongoDB**: NoSQL database (integrated via `djongo`).
- **Simple JWT**: JSON Web Token authentication for Django REST Framework.
- **Gunicorn** & **WhiteNoise**: Production-grade server and static file management.

### DevOps & Tools

- **Docker**: Containerization for consistent development and deployment environments.
- **Git**: Version control.

---

## 📂 Project Structure

```bash
HRMS/
├── backend/                # Django Backend
│   ├── hrms_core/          # Project settings and configuration
│   ├── employees/          # Employee management app
│   ├── attendance/         # Attendance tracking app
│   ├── leaves/             # Leave management app
│   ├── requirements.txt    # Python dependencies
│   ├── manage.py           # Django management script
│   └── Dockerfile          # Backend Dockerfile
│
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components (Layout, UI)
│   │   ├── pages/          # Page components (Dashboard, Employees, etc.)
│   │   ├── context/        # Global state (AuthContext)
│   │   ├── services/       # API configuration
│   │   └── App.js          # Main application component
│   ├── package.json        # Node dependencies
│   └── tailwind.config.js  # Tailwind configuration
│
└── docker-compose.yml      # Orchestration for multi-container Docker app
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (Local instance or Atlas URI)
- **Docker** (Optional, for containerized setup)

### Option 1: Local Development Setup

#### 1. Backend Setup

Navigate to the backend directory and set up the virtual environment.

```bash
cd backend
python -m venv venv
# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure Environment Variables:
Create a `.env` file in the `backend/` directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
MONGODB_URL=mongodb://localhost:27017/hrms_db
ALLOWED_HOSTS=*
```

Run Migrations and Start Server:

```bash
python manage.py migrate
python manage.py runserver
```

The backend will run at `http://localhost:8000`.

#### 2. Frontend Setup

Open a new terminal and navigate to the frontend directory.

```bash
cd frontend
npm install
```

Start the React Development Server:

```bash
npm start
```

The frontend will run at `http://localhost:3000`.

---

### Option 2: Docker Setup (Recommended for Deployment)

Ensure Docker and Docker Compose are installed.

1. **Build and Run Containers**:

   ```bash
   docker-compose up --build
   ```

2. **Access the Application**:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

---

## 📡 API Endpoints

| Method         | Endpoint                    | Description                    |
| :------------- | :-------------------------- | :----------------------------- |
| **Auth**       |                             |                                |
| `POST`         | `/api/token/`               | Obtain Access & Refresh Tokens |
| `POST`         | `/api/token/refresh/`       | Refresh Access Token           |
| **Employees**  |                             |                                |
| `GET`          | `/api/employees/`           | List all employees             |
| `POST`         | `/api/employees/`           | Create a new employee          |
| `DELETE`       | `/api/employees/{id}/`      | Delete an employee             |
| **Attendance** |                             |                                |
| `GET`          | `/api/attendance/`          | List attendance records        |
| `POST`         | `/api/attendance/`          | Mark attendance                |
| **Leaves**     |                             |                                |
| `GET`          | `/api/leaves/`              | List leave requests            |
| `POST`         | `/api/leaves/`              | Apply for leave                |
| `PATCH`        | `/api/leaves/{id}/approve/` | Approve a leave request        |
| `PATCH`        | `/api/leaves/{id}/reject/`  | Reject a leave request         |

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and create a pull request for any feature enhancements or bug fixes.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
