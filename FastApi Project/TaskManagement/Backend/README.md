# Task Management API

A production-level Backend API built with **FastAPI**, **PostgreSQL**, and **JWT Authentication**.

## 🚀 Features

-   **User Authentication:** Secure registration and login using JWT (JSON Web Tokens).
-   **Task CRUD:** Full Create, Read, Update, and Delete operations for tasks.
-   **Data Security:** Password hashing with `bcrypt`.
-   **Ownership Control:** Users can only access, edit, or delete their own tasks.
-   **Database:** SQLAlchemy ORM with PostgreSQL.
-   **Validation:** Robust request/response validation using Pydantic.
-   **Auto-Documentation:** Interactive API docs via Swagger UI and ReDoc.

## 🛠️ Project Structure

```text
Backend/
├── app/
│   ├── core/           # Config, Security, and Utils
│   ├── database/       # DB Connection and Session
│   ├── Model/          # SQLAlchemy Models
│   ├── router/         # API Route Handlers
│   ├── Schema/         # Pydantic Schemas
│   └── main.py         # App Entry Point
├── .env                # Environment Variables
├── requirement.txt     # Dependencies
└── venv/               # Virtual Environment
```

## ⚙️ Installation & Setup

1.  **Clone the repository** (or navigate to the directory).
2.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    ```
3.  **Activate Virtual Environment:**
    -   **Windows:** `.\venv\Scripts\activate`
    -   **Mac/Linux:** `source venv/bin/activate`
4.  **Install Dependencies:**
    ```bash
    pip install -r requirement.txt
    ```
5.  **Environment Variables:**
    Update the `.env` file with your database credentials:
    ```env
    DATABASE_URL=postgresql://user:password@localhost/dbname
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    ```

## 🏃 Running the Application

Start the server using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

> **Note:** Ensure there is no space between `--` and `reload`.

## 📖 API Documentation

Once the server is running, you can access the interactive documentation at:
-   **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## 🔒 Endpoints

### Authentication
-   `POST /users/`: Register a new user.
-   `POST /login`: Login and receive an access token.

### Tasks
-   `GET /tasks/`: Retrieve all tasks for the current user.
-   `POST /tasks/`: Create a new task.
-   `GET /tasks/{id}`: Get a specific task.
-   `PUT /tasks/{id}`: Update a task.
-   `DELETE /tasks/{id}`: Delete a task.
