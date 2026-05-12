# ERP Dynamic Form Builder Module

This module provides a production-grade dynamic form builder, acting as a core feature for the ERP system operations. It allows users to create forms dynamically from the UI, manage form properties, and persist dynamic configurations without altering the physical database schema.

## 🏗️ Architecture Overview

The system is built on a **Monolithic Architecture** tailored for maintainability, simplicity, and scaling.

- **Frontend**: React (Vanilla JavaScript), Vite, TailwindCSS (Glassmorphism aesthetics).
- **Backend**: FastAPI (Python 3.12+), SQLAlchemy 2.0 (async), Pydantic v2.
- **Database**: PostgreSQL (Hybrid relational tables + `JSONB` for dynamic structures).
- **Infrastructure**: Fully Dockerized with multi-stage NGINX build for the frontend.

---

## ✨ Features Implemented

### 1. Dynamic Database Design
- Utilizes **PostgreSQL `JSONB`** columns (`form_schema` and `submission_data`) to handle infinitely flexible forms without running costly `ALTER TABLE` migrations.

### 2. Form Builder Engine (Frontend)
- **State Management**: Zustand was removed in favor of native **React Context API** for simpler developer onboarding and maintenance.
- **Vanilla JavaScript**: Codebase was fully converted from TypeScript to standard `.jsx` React.
- **Components**:
  - `Sidebar.jsx`: Drag-and-drop tool palette.
  - `Canvas.jsx`: Live rendering canvas for dynamic schemas.
  - `PropertiesPanel.jsx`: Context-aware settings editor for customizing individual form fields (e.g., options, placeholders, requirements).

### 3. FastAPI Backend
- Fully async routing and database interactions via `asyncpg`.
- Pydantic models for strict payload validation.

---

## 🐳 Running with Docker (Recommended)

The easiest way to start the entire ecosystem is through Docker Compose.

1. Ensure Docker and Docker Compose are installed.
2. Run the following command from the project root:

```bash
docker-compose up --build -d
```

### Services Access:
- **Frontend App**: [http://localhost](http://localhost) (Served via NGINX)
- **Backend API**: [http://localhost:8000/api](http://localhost:8000/api)
- **Swagger Documentation**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
- **Database**: PostgreSQL running internally on `5432`.

To stop the services:
```bash
docker-compose down
```

---

## 💻 Local Development (Without Docker)

If you wish to run the servers locally for development purposes, follow these steps:

### Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and configure your `.env` file based on your local PostgreSQL credentials (A template has been provided in the directory).
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install the necessary Node packages (Requires Node.js):
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```

*(Note: Ensure you are using Node >=20.19 or >=22.12 to support the latest Vite version).*

---

## 📂 Project Structure

```text
Form/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # REST Endpoints
│   │   ├── core/             # Configuration (.env mapping)
│   │   ├── db/               # Async Engine & Session
│   │   ├── models/           # SQLAlchemy DB Models (JSONB)
│   │   └── schemas/          # Pydantic Validation
│   ├── Dockerfile            # Python 3.12 Image
│   ├── .env                  # DB Credentials
│   └── requirements.txt
│
├── frontend/                 # React UI
│   ├── src/
│   │   ├── context/          # React Context API (State)
│   │   ├── modules/          # Core Builder Components
│   │   ├── App.jsx           # Provider Wrapper
│   │   └── main.jsx
│   ├── Dockerfile            # Multi-stage NGINX build
│   └── package.json
│
└── docker-compose.yml        # Orchestration Config
```
