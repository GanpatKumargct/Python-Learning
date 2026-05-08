# Mini-ATS (Applicant Tracking System)

A lightweight Applicant Tracking System featuring a modern React frontend and a FastAPI backend with SQLite. It allows you to manage job postings and track candidates through a drag-and-drop pipeline board.

## Project Structure
- `frontend/` - React frontend powered by Vite, Tailwind CSS, and `react-router-dom`. Features a Candidate Job Listing UI and a drag-and-drop HR Dashboard.
- `Backend/` - Python FastAPI backend providing RESTful endpoints, with an SQLite database and SQLAlchemy ORM.

## Setup Instructions

### 1. Frontend Setup
Make sure you have Node.js installed.

```bash
cd frontend
npm install
npm run dev
```
The React development server will start on `http://localhost:5173/`.

### 2. Backend Setup
Make sure you have Python installed.

```bash
cd Backend

# Activate the virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux (if applicable):
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload
```
The FastAPI server will start on `http://127.0.0.1:8000`. You can access the interactive Swagger API documentation at `http://127.0.0.1:8000/docs`.

## Backend API Endpoints
- **Jobs**:
  - `GET /jobs/` - Get a list of all jobs.
  - `POST /jobs/` - Create a new job.
  - `PUT /jobs/{job_id}/status` - Toggle a job's open/closed status.
- **Applications**:
  - `GET /applications/` - Get all applications.
  - `POST /applications/` - Create a new application.
  - `PUT /applications/{app_id}/stage` - Move an application to a different pipeline stage (automatically logs history).
