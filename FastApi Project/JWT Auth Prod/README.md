# Production Level JWT Authentication with RBAC

This repository demonstrates a production-grade implementation of JSON Web Token (JWT) authentication, featuring Role-Based Access Control (RBAC). It includes a fully functional **FastAPI** backend and a **React** frontend.

## 🚀 Tech Stack

- **Backend:** FastAPI, PostgreSQL, SQLAlchemy (ORM), Pydantic, Passlib (bcrypt), Python-jose
- **Frontend:** React, Vite, React Router, Axios, Context API
- **Authentication:** OAuth2 with Password (and hashing), Bearer JWT tokens

---

## 🛠️ Features Implemented

1. **User Registration & Login:** 
   - New users can register and login securely. Passwords are hashed using `bcrypt`.
2. **Role-Based Access Control (RBAC):**
   - **External Users:** Default access level upon registration.
   - **Admin (Internal):** Special role that grants access to the Admin Panel.
   - Admins can dynamically create internal roles (e.g., *HR*, *Process Eng*, *Manager*, *Founder*).
   - Admins can assign these roles to users to grant specific access levels across the application.
3. **Production Standard Practices:**
   - **Environment Variables:** Credentials and Secret Keys are isolated in a `.env` file.
   - **Dependency Injection:** Database sessions and token validations are managed via FastAPI dependencies.
   - **Logging:** Both console and file logging (`app.log`) are implemented using standard Python logging.
   - **Structured Architecture:** The backend separates concerns into `core`, `db`, `models`, `schemas`, `crud`, and `api` layers.

---

## 📁 Project Structure

```text
├── Back-End/                   # FastAPI Backend
│   ├── app/
│   │   ├── api/                # API Routers & Dependencies
│   │   │   ├── deps.py         # Authentication & RBAC Dependencies
│   │   │   └── routes/         # Endpoint modules (auth, users, roles)
│   │   ├── core/               # Configuration & Security (JWT, Hashing)
│   │   ├── crud/               # Database operations (Create, Read, Update, Delete)
│   │   ├── db/                 # Database setup and SQLAlchemy Models
│   │   ├── schemas/            # Pydantic models for data validation
│   │   ├── utils/              # Utilities (Logging)
│   │   └── main.py             # FastAPI entry point
│   ├── requirements.txt
│   └── .env                    # Environment variables
└── Front-End/                  # React Frontend
    ├── src/
    │   ├── api/                # Axios instance configuration
    │   ├── components/         # React Views (Login, Register, Dashboard, AdminPanel)
    │   ├── context/            # React Context API for global auth state
    │   ├── App.jsx             # Main application & routing logic
    │   └── main.jsx
    ├── package.json
    └── vite.config.js
```

---

## ⚙️ How to Run Locally

### 1. Database Setup
Make sure you have **PostgreSQL** installed and running on your local machine. Create a database named `jwt_auth_db`.
```sql
CREATE DATABASE jwt_auth_db;
```

### 2. Backend Setup
Navigate into the backend directory and set up your virtual environment.

```bash
cd Back-End

# Create virtual environment (optional but recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload
```
The API will be running at `http://localhost:8000`. You can access the automatic Swagger UI documentation at `http://localhost:8000/docs`.

### 3. Creating the First Admin
Since only Admins can create new roles and assign them, you need to manually assign the "Admin" role to your first user.
1. Register a user via the React frontend or Swagger UI.
2. In your PostgreSQL database, manually create an 'Admin' role and link it to your user:
```sql
INSERT INTO roles (name, description) VALUES ('Admin', 'Super Administrator');
-- Assuming your user ID is 1 and the Admin role ID is 1
UPDATE users SET role_id = 1 WHERE id = 1;
```

### 4. Frontend Setup
Open a new terminal, navigate to the frontend directory, install packages, and start the Vite dev server.

```bash
cd Front-End

# Install Node dependencies
npm install

# Start the development server
npm run dev
```
The React app will be running at `http://localhost:5173` (or similar port).

---

## 📝 Code Comments for Learning
Throughout the codebase, specific comments have been left to explain *why* certain practices are used. These are intended to help developers reference this project when building out their own authentication systems. Areas like `deps.py` (FastAPI Dependencies) and `AuthContext.jsx` (React global state) are specifically annotated to highlight standard industry practices.
