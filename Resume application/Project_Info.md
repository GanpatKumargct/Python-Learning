# ATS Module — Technical Requirements Document & System Requirements Specification
> **ERP System | Aerospace Company**
> Document Version: 1.0 | Status: Draft | Date: 2026-05-10
> Audience: Junior Developers (Frontend & Backend)
> Classification: Internal – Confidential

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Monorepo Folder Structure](#2-monorepo-folder-structure)
3. [Engineering Standards](#3-engineering-standards)
4. [Database Design](#4-database-design)
5. [Backend — FastAPI](#5-backend--fastapi)
6. [Frontend — React](#6-frontend--react)
7. [Dynamic Form Builder](#7-dynamic-form-builder)
8. [Authentication & RBAC](#8-authentication--rbac)
9. [File Storage](#9-file-storage)
10. [Email System](#10-email-system)
11. [Docker & Infrastructure](#11-docker--infrastructure)
12. [API Reference Summary](#12-api-reference-summary)
13. [Environment Variables](#13-environment-variables)
14. [README Template](#14-readme-template)

---

## 1. Project Overview

### 1.1 What You Are Building

An **Applicant Tracking System (ATS)** that is **one module** of a larger ERP platform for an aerospace company. The ERP will eventually include modules like Inventory Management, Finance, HR, etc. This document covers only the ATS module, but all decisions about structure must keep future modules in mind.

### 1.2 Core Capabilities (ATS Module)

| # | Capability | Description |
|---|---|---|
| 1 | **Dynamic Form Builder** | Admin/PTC builds forms like Google Forms. Each form gets its own response table in PostgreSQL. |
| 2 | **Hiring Requisition** | Approval chain: Project Director → Chief of Staff → Founder → PTC |
| 3 | **Recruitment Pipeline** | 5 stages: Screening → Fitment Evaluation → Technical Interview → PTC Round → Founder Round |
| 4 | **Role-Based Access** | Admin, PTC, Founder, Director, Hiring Manager, Supporting Member, External Candidate |
| 5 | **File Uploads** | CVs, task submissions stored in S3-compatible storage; DB stores links only |
| 6 | **Email Notifications** | Templated emails with WYSIWYG editor, per-stage triggers |
| 7 | **Zoho Integrations** | Zoho People (org chart/teams) + Zoho Bookings (interview scheduling) |
| 8 | **Candidate Portal** | External candidates fill forms, upload documents, receive email updates |
| 9 | **Two Data Views** | Kanban (by pipeline stage) and Tabular (sortable/filterable table) |

### 1.3 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, React Router v6, TanStack Query, Tailwind CSS, plain JavaScript (ES2022+) |
| Backend | Python 3.12, FastAPI, SQLAlchemy 2.x (async), Alembic |
| Database | PostgreSQL 16 |
| Cache / Queue | Redis 7 (session cache, email queue via Celery) |
| File Storage | MinIO (self-hosted S3-compatible) |
| Email | SMTP via Celery task; Jinja2 templates |
| Auth | JWT (access + refresh tokens); OTP via Redis |
| Containerisation | Docker + Docker Compose |
| Proxy | Nginx (production) |

---

## 2. Monorepo Folder Structure

### 2.1 Structure Philosophy

The project follows a **monorepo with explicit workspace separation** — `frontend/` and `backend/` are first-class top-level directories. This is the pattern used by companies like Shopify, Linear, and Vercel for internal platforms: one repository, clear ownership boundaries, shared infra config, independent dependency management.

**Key principles applied here:**

- `frontend/` and `backend/` are completely self-contained — each has its own `package.json` / `requirements.txt`, its own `Dockerfile`, its own tests, its own `.env.example`.
- A developer working only on the frontend never needs to enter `backend/` and vice versa.
- Infrastructure (`infra/`) and documentation (`docs/`) live at the root — owned by no single team.
- Every new ERP module (Inventory, Finance) adds a subfolder inside `frontend/src/modules/` and `backend/app/modules/` — the root structure never changes.
- CI/CD pipelines can trigger independently per directory (`backend/**` changed → run backend pipeline; `frontend/**` changed → run frontend pipeline).

---

### 2.2 Full Directory Tree

```
erp-aerospace/                          ← Git repository root
│
│   ── Root-level files ──
├── .gitignore                          ← Covers Python, Node, env files, OS artifacts
├── .env.example                        ← Shared vars used by docker-compose only
├── README.md                           ← Developer onboarding (quick start)
├── CONTRIBUTING.md                     ← Branch strategy, commit convention, PR rules
│
│   ── Frontend workspace ──
├── frontend/
│   ├── .env.example                    ← VITE_API_URL, VITE_APP_NAME etc.
│   ├── .eslintrc.cjs                   ← ESLint config (react + hooks preset)
│   ├── .prettierrc                     ← Prettier formatting rules
│   ├── index.html                      ← Vite HTML entry
│   ├── package.json                    ← All frontend dependencies
│   ├── vite.config.js                  ← Vite + path aliases (@/ → src/)
│   ├── tailwind.config.js              ← Tailwind + custom design tokens
│   ├── postcss.config.cjs
│   ├── Dockerfile                      ← Multi-stage: build → nginx serve
│   ├── Dockerfile.dev                  ← Dev: hot-reload with Vite dev server
│   ├── nginx.conf                      ← Frontend nginx config (SPA fallback)
│   │
│   ├── public/                         ← Static assets (favicon, robots.txt, og images)
│   │   ├── favicon.ico
│   │   └── robots.txt
│   │
│   └── src/
│       ├── main.jsx                    ← App entry: ReactDOM.createRoot
│       ├── App.jsx                     ← Router setup, QueryClientProvider, auth guard
│       │
│       ├── modules/                    ← One folder per ERP module
│       │   │
│       │   ├── shared/                 ← Cross-module reusable code (NOT module-specific)
│       │   │   ├── components/         ← UI primitives used everywhere
│       │   │   │   ├── ui/             ← Headless/base components
│       │   │   │   │   ├── Button.jsx
│       │   │   │   │   ├── Input.jsx
│       │   │   │   │   ├── Modal.jsx
│       │   │   │   │   ├── Table.jsx
│       │   │   │   │   ├── Badge.jsx
│       │   │   │   │   ├── Spinner.jsx
│       │   │   │   │   ├── Toast.jsx
│       │   │   │   │   └── index.js    ← barrel export
│       │   │   ├── layouts/
│       │   │   │   ├── AppLayout.jsx   ← Sidebar + topbar shell for staff
│       │   │   │   ├── PublicLayout.jsx ← Minimal layout for candidate forms
│       │   │   │   └── AuthLayout.jsx  ← Login / register pages
│       │   │   ├── guards/
│       │   │   │   ├── AuthGuard.jsx   ← Redirect to /login if no token
│       │   │   │   └── RoleGuard.jsx   ← 403 or redirect if role not allowed
│       │   │   ├── hooks/
│       │   │   │   ├── useAuth.js      ← Read from auth store + helper methods
│       │   │   │   └── useToast.js
│       │   │   └── constants/
│       │   │       ├── roles.js        ← ROLES object, ROLE_LABELS map
│       │   │       └── routes.js       ← ROUTE_PATHS constants (avoid magic strings)
│       │   │
│       │   ├── ats/                    ← ATS module (Applicant Tracking System)
│       │   │   │
│       │   │   ├── pages/              ← Route-level components (one per page/view)
│       │   │   │   ├── DashboardPage.jsx
│       │   │   │   ├── requisitions/
│       │   │   │   │   ├── RequisitionListPage.jsx
│       │   │   │   │   ├── RequisitionNewPage.jsx
│       │   │   │   │   └── RequisitionDetailPage.jsx
│       │   │   │   ├── pipeline/
│       │   │   │   │   ├── PipelineKanbanPage.jsx
│       │   │   │   │   ├── PipelineTablePage.jsx
│       │   │   │   │   └── CandidateDetailPage.jsx
│       │   │   │   ├── forms/
│       │   │   │   │   ├── FormBuilderListPage.jsx
│       │   │   │   │   ├── FormBuilderEditorPage.jsx  ← drag-and-drop editor
│       │   │   │   │   ├── FormResponsesPage.jsx
│       │   │   │   │   └── CandidateFormPage.jsx      ← public, no auth
│       │   │   │   ├── email-templates/
│       │   │   │   │   └── EmailTemplatesPage.jsx
│       │   │   │   └── admin/
│       │   │   │       ├── UsersPage.jsx
│       │   │   │       └── SystemConfigPage.jsx
│       │   │   │
│       │   │   ├── components/         ← ATS-specific reusable UI components
│       │   │   │   ├── pipeline/
│       │   │   │   │   ├── KanbanBoard.jsx
│       │   │   │   │   ├── KanbanCard.jsx
│       │   │   │   │   ├── StageAdvanceModal.jsx
│       │   │   │   │   └── RejectionRemarkModal.jsx
│       │   │   │   ├── forms/
│       │   │   │   │   ├── FormFieldPalette.jsx       ← drag source: field types
│       │   │   │   │   ├── FormFieldList.jsx           ← drop target: ordered fields
│       │   │   │   │   ├── FormFieldEditor.jsx         ← right panel: field config
│       │   │   │   │   ├── FormFieldRenderer.jsx       ← renders a field for preview/fill
│       │   │   │   │   └── FieldTypes/
│       │   │   │   │       ├── TextField.jsx
│       │   │   │   │       ├── SelectField.jsx
│       │   │   │   │       ├── FileUploadField.jsx
│       │   │   │   │       └── ...
│       │   │   │   ├── requisitions/
│       │   │   │   │   ├── ApprovalTimeline.jsx
│       │   │   │   │   └── RequisitionStatusBadge.jsx
│       │   │   │   └── admin/
│       │   │   │       ├── InviteUserModal.jsx
│       │   │   │       └── UserRoleBadge.jsx
│       │   │   │
│       │   │   ├── hooks/              ← TanStack Query hooks (data fetching)
│       │   │   │   ├── useRequisitions.js
│       │   │   │   ├── usePipeline.js
│       │   │   │   ├── useForms.js
│       │   │   │   ├── useCandidates.js
│       │   │   │   └── useEmailTemplates.js
│       │   │   │
│       │   │   ├── services/           ← Raw API call functions (axios wrappers)
│       │   │   │   ├── requisitionsApi.js
│       │   │   │   ├── pipelineApi.js
│       │   │   │   ├── formsApi.js
│       │   │   │   └── adminApi.js
│       │   │   │
│       │   │   └── constants/          ← ATS-specific constants (no types/ folder needed)
│       │   │       ├── pipelineStages.js   ← stage names, labels, order
│       │   │       └── formFieldTypes.js   ← field type definitions + icons
│       │   │
│       │   └── (future modules: inventory/, finance/, hr/)
│       │       └── ← same structure: pages/, components/, hooks/, services/, constants/
│       │
│       ├── lib/                        ← Non-module technical utilities
│       │   ├── apiClient.js            ← Axios instance + interceptors
│       │   ├── queryClient.js          ← TanStack QueryClient singleton
│       │   └── utils.js                ← Date formatters, string helpers, etc.
│       │
│       ├── store/                      ← Zustand global state (minimal — prefer server state)
│       │   ├── authStore.js            ← user, accessToken, setAuth, logout
│       │   └── uiStore.js              ← sidebar open/close, active module
│       │
│       ├── routes/
│       │   ├── index.jsx               ← createBrowserRouter config
│       │   ├── atsRoutes.jsx           ← ATS route tree (lazy-loaded pages)
│       │   └── (future: inventoryRoutes.jsx, financeRoutes.jsx)
│       │
│       └── styles/
│           └── globals.css             ← Tailwind base + custom CSS variables
│
│   ── Backend workspace ──
├── backend/
│   ├── .env.example                    ← All backend env vars with descriptions
│   ├── .flake8                         ← Linting config (max-line-length, ignores)
│   ├── pyproject.toml                  ← Black formatter config + isort config
│   ├── requirements.txt                ← Production dependencies (pinned versions)
│   ├── requirements-dev.txt            ← Dev/test dependencies (pytest, httpx, etc.)
│   ├── Dockerfile                      ← Multi-stage: slim Python image
│   ├── Dockerfile.dev                  ← Dev: uvicorn --reload
│   │
│   ├── alembic.ini                     ← Alembic config (points to app/core/database.py)
│   │
│   ├── app/
│   │   ├── main.py                     ← FastAPI app factory, router registration, CORS
│   │   │
│   │   ├── core/                       ← Framework-level code, no business logic
│   │   │   ├── __init__.py
│   │   │   ├── config.py               ← Pydantic Settings (reads .env)
│   │   │   ├── database.py             ← Async SQLAlchemy engine, session, Base
│   │   │   ├── security.py             ← JWT encode/decode, bcrypt hash/verify
│   │   │   ├── dependencies.py         ← get_db, get_current_user, require_roles()
│   │   │   ├── exceptions.py           ← Custom HTTP exceptions + global handler
│   │   │   ├── logging.py              ← Structured JSON logging (production)
│   │   │   └── storage.py              ← MinIO/S3 client, presigned URL helpers
│   │   │
│   │   ├── modules/                    ← One package per ERP module + shared modules
│   │   │   │
│   │   │   ├── auth/                   ← Shared across all ERP modules
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py           ← /auth/* endpoints
│   │   │   │   ├── service.py          ← Login, OTP, token refresh logic
│   │   │   │   ├── schemas.py          ← Pydantic request/response models
│   │   │   │   └── models.py           ← SQLAlchemy: users, refresh_tokens, auth_otp
│   │   │   │
│   │   │   ├── admin/                  ← User + role management (Admin only)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py
│   │   │   │   ├── service.py
│   │   │   │   ├── schemas.py
│   │   │   │   └── models.py           ← (reuses users model from auth)
│   │   │   │
│   │   │   ├── ats/                    ← ATS module
│   │   │   │   ├── __init__.py
│   │   │   │   │
│   │   │   │   ├── requisitions/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── router.py       ← /requisitions/* endpoints
│   │   │   │   │   ├── service.py      ← Business logic (approval chain, status transitions)
│   │   │   │   │   ├── schemas.py      ← Pydantic I/O models
│   │   │   │   │   └── models.py       ← SQLAlchemy: hiring_requisitions, approvals
│   │   │   │   │
│   │   │   │   ├── pipeline/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── router.py       ← /pipelines/* endpoints
│   │   │   │   │   ├── service.py      ← Stage transitions, rejection logic, notifications
│   │   │   │   │   ├── schemas.py
│   │   │   │   │   └── models.py       ← SQLAlchemy: pipelines, stage_history
│   │   │   │   │
│   │   │   │   ├── candidates/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── router.py       ← /candidates/* endpoints
│   │   │   │   │   ├── service.py
│   │   │   │   │   ├── schemas.py
│   │   │   │   │   └── models.py       ← SQLAlchemy: candidates, submissions
│   │   │   │   │
│   │   │   │   ├── forms/              ← Dynamic form builder
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── router.py       ← /forms/* + /forms/:id/submit (public)
│   │   │   │   │   ├── service.py      ← DDL table creation, response insert
│   │   │   │   │   ├── schemas.py
│   │   │   │   │   └── models.py       ← SQLAlchemy: forms, form_fields, file_uploads
│   │   │   │   │
│   │   │   │   ├── emails/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── router.py       ← /email-templates/* endpoints
│   │   │   │   │   ├── service.py      ← Template CRUD + version history
│   │   │   │   │   ├── schemas.py
│   │   │   │   │   └── models.py       ← SQLAlchemy: email_templates, history
│   │   │   │   │
│   │   │   │   └── referrals/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── router.py
│   │   │   │       ├── service.py
│   │   │   │       ├── schemas.py
│   │   │   │       └── models.py
│   │   │   │
│   │   │   └── (future: inventory/, finance/, hr/)
│   │   │       └── ← same structure: router, service, schemas, models
│   │   │
│   │   └── workers/                    ← Celery async task workers
│   │       ├── __init__.py
│   │       ├── celery_app.py           ← Celery instance + config
│   │       └── tasks/
│   │           ├── __init__.py
│   │           ├── email_tasks.py      ← send_email task (SMTP)
│   │           └── notification_tasks.py ← internal alert tasks
│   │
│   ├── migrations/                     ← Alembic migrations (previously named alembic/)
│   │   ├── env.py                      ← Imports all models, configures target_metadata
│   │   ├── script.py.mako
│   │   └── versions/                   ← Auto-generated migration files
│   │       └── 0001_create_ats_tables.py
│   │
│   ├── tests/
│   │   ├── conftest.py                 ← Pytest fixtures: test DB, test client, seed data
│   │   ├── unit/                       ← Pure function tests (no DB)
│   │   │   ├── test_security.py
│   │   │   ├── test_form_ddl.py
│   │   │   └── test_pipeline_rules.py
│   │   └── integration/                ← Tests with real DB (use pytest-asyncio)
│   │       ├── test_auth_flow.py
│   │       ├── test_requisition_approval.py
│   │       └── test_form_submission.py
│   │
│   └── scripts/
│       ├── seed_db.py                  ← Creates admin user, default roles, email templates
│       └── create_minio_bucket.py      ← Idempotent MinIO bucket + policy setup
│
│   ── Infrastructure (shared) ──
├── infra/
│   ├── docker-compose.yml              ← Development: all services + volume mounts
│   ├── docker-compose.prod.yml         ← Production: no volume mounts, restart policies
│   ├── nginx/
│   │   ├── nginx.dev.conf              ← Dev proxy (forwards /api → backend:8000)
│   │   └── nginx.prod.conf             ← Prod: SSL termination, gzip, cache headers
│   └── minio/
│       └── init.sh                     ← Creates bucket on first run via mc (MinIO client)
│
│   ── Documentation ──
└── docs/
    ├── ATS_TRD_SRS.md                  ← This document
    ├── BRD_ATS.html                    ← Business requirements (stakeholder-facing)
    └── diagrams/
        ├── approval-flow.png
        └── pipeline-stages.png
```

---

### 2.3 Why This Structure (Decisions Explained)

**`frontend/` and `backend/` at root level, not nested**

Real companies (Linear, Vercel, Shopify's internal tools) do this because:
- Docker build contexts are clean: `docker build ./frontend` or `docker build ./backend` — no path games.
- CI pipelines use path filters (`on: paths: ['backend/**']`) to avoid rebuilding the frontend when only Python changed.
- New developer onboarding is obvious — `cd frontend && npm install` or `cd backend && pip install`.

**`modules/` inside both frontend and backend**

Every feature (ATS, future Inventory, Finance) is self-contained inside its `modules/ats/` folder. This prevents what's called "feature creep into shared space" — a common mistake where junior devs put ATS-specific code into shared utilities because it seems reusable but isn't.

Rule: **code lives in the most specific folder that owns it.**

```
Is it used by more than one ERP module?  → shared/
Is it only used by ATS?                  → modules/ats/
Is it only used by the Pipeline feature? → modules/ats/pipeline/ (or components/pipeline/)
```

**`services/` inside `frontend/src/modules/ats/`**

Separating API call functions (`formsApi.js`) from query hooks (`useForms.js`) means:
- `services/` = raw axios calls, testable in isolation.
- `hooks/` = TanStack Query wrappers, control cache keys and loading/error states.
- Pages import hooks, never API services directly.

**`migrations/` at `backend/` root (not nested inside `app/`)**

Alembic is a CLI tool — it's easier to run `alembic upgrade head` from `backend/` than to `cd` into `app/`. Keeps migration commands consistent: `cd backend && alembic upgrade head`.

**`infra/` at repo root**

Infrastructure is owned by no single team. Both frontend and backend Docker containers are configured here. A Platform/DevOps engineer can modify `docker-compose.prod.yml` without touching application code.

**Separate `Dockerfile` and `Dockerfile.dev`**

- `Dockerfile.dev` runs dev server with hot reload (Vite `--watch` / uvicorn `--reload`).
- `Dockerfile` is multi-stage production build — frontend builds to static HTML/JS/CSS served by nginx; backend builds a lean image without dev tools.
- Never use the dev Dockerfile in production. The `docker-compose.prod.yml` always references `Dockerfile`.

---

## 3. Engineering Standards

### 3.1 `.gitignore`

Create `erp-aerospace/.gitignore` with:

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
env/
*.egg-info/
dist/
build/

# Node
node_modules/
dist/
.cache/
*.local

# Environment files — NEVER commit
.env
.env.local
.env.*.local
*.env

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test / coverage
.coverage
htmlcov/
.pytest_cache/
coverage/

# Alembic — don't commit generated files
# (versions/ SHOULD be committed)

# Docker volumes
postgres_data/
minio_data/
redis_data/
```

### 3.2 `.env.example` (root)

```env
# Postgres
POSTGRES_USER=erp_user
POSTGRES_PASSWORD=changeme
POSTGRES_DB=erp_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=your-256-bit-secret-here
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# MinIO / S3
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=erp-files
MINIO_USE_SSL=false

# Email (SMTP)
SMTP_HOST=smtp.yourprovider.com
SMTP_PORT=587
SMTP_USER=noreply@company.com
SMTP_PASSWORD=changeme
EMAIL_FROM_NAME=Aerospace Recruitment

# Zoho
ZOHO_CLIENT_ID=
ZOHO_CLIENT_SECRET=
ZOHO_PEOPLE_API_BASE=https://people.zoho.com/api/v2
ZOHO_BOOKINGS_API_BASE=https://bookings.zoho.com/api/v1

# App
APP_ENV=development
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
CORS_ORIGINS=["http://localhost:5173"]
```

### 3.3 Git Branching Convention

```
main          — production-ready code
develop       — integration branch
feature/ats-form-builder
feature/ats-pipeline-kanban
fix/ats-otp-expiry
```

### 3.4 Commit Message Convention

```
feat(ats): add dynamic form builder API
fix(auth): OTP expiry not being checked
docs: update ATS TRD with form schema
chore: update requirements.txt
```

---

## 4. Database Design

### 4.1 Key Design Principles

- All primary keys use `UUID` (not serial integers) — safer for multi-module ERP.
- All tables have `created_at` and `updated_at` timestamps.
- Soft deletes via `deleted_at` nullable timestamp where appropriate.
- The dynamic form builder generates new response tables at runtime via DDL.
- Form metadata is stored in fixed tables; responses go into dynamically created tables.

### 4.2 Schema: Auth & Users

```sql
-- Roles enum (extensible for future ERP modules)
CREATE TYPE user_role AS ENUM (
  'admin',
  'ptc',
  'founder',
  'project_director',
  'chief_of_staff',
  'hiring_manager',
  'supporting_member'
);

CREATE TABLE users (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT UNIQUE NOT NULL,
  full_name     TEXT NOT NULL,
  password_hash TEXT,                   -- NULL for candidates (magic link only)
  role          user_role NOT NULL,
  department    TEXT,                   -- optional, from Zoho People
  is_active     BOOLEAN DEFAULT TRUE,
  created_by    UUID REFERENCES users(id),
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW(),
  deleted_at    TIMESTAMPTZ             -- soft delete
);

-- OTP / magic link store (Redis is primary, this is fallback audit)
CREATE TABLE auth_otp (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email       TEXT NOT NULL,
  otp_hash    TEXT NOT NULL,
  purpose     TEXT NOT NULL,            -- 'login', 'register', 'magic_link'
  expires_at  TIMESTAMPTZ NOT NULL,
  used_at     TIMESTAMPTZ,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Refresh tokens
CREATE TABLE refresh_tokens (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
  token_hash  TEXT UNIQUE NOT NULL,
  expires_at  TIMESTAMPTZ NOT NULL,
  revoked_at  TIMESTAMPTZ,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.3 Schema: Candidates (External)

```sql
CREATE TABLE candidates (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email         TEXT UNIQUE NOT NULL,    -- unique identifier
  full_name     TEXT NOT NULL,
  phone         TEXT,
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.4 Schema: Dynamic Form Builder

Three fixed tables govern all forms. Responses go into dynamically created tables.

```sql
-- TABLE 1: Form Registry
CREATE TABLE forms (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title           TEXT NOT NULL,
  description     TEXT,                  -- remarks / short description
  department      TEXT,                  -- which dept uses this form
  module          TEXT NOT NULL DEFAULT 'ats',  -- 'ats', 'inventory', etc.
  response_table  TEXT UNIQUE NOT NULL,  -- dynamically created table name e.g. 'form_responses_a1b2c3'
  is_active       BOOLEAN DEFAULT TRUE,
  version         INTEGER DEFAULT 1,
  created_by      UUID REFERENCES users(id),
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- TABLE 2: Form Fields (metadata / schema of the form)
CREATE TABLE form_fields (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  form_id         UUID REFERENCES forms(id) ON DELETE CASCADE,
  field_key       TEXT NOT NULL,         -- column name used in response table e.g. 'first_name'
  label           TEXT NOT NULL,         -- display label e.g. 'First Name'
  field_type      TEXT NOT NULL,         -- 'text', 'textarea', 'number', 'email', 'date',
                                         -- 'select', 'multi_select', 'checkbox', 'radio',
                                         -- 'file_upload', 'section_header'
  is_required     BOOLEAN DEFAULT FALSE,
  options         JSONB,                 -- for select/radio/checkbox: [{"label":"A","value":"a"}]
  validation      JSONB,                 -- {"min":0,"max":100,"pattern":"^[A-Z]"} etc.
  display_order   INTEGER NOT NULL,
  column_type     TEXT DEFAULT 'TEXT',   -- PostgreSQL column type for response table
                                         -- 'TEXT', 'INTEGER', 'BOOLEAN', 'TIMESTAMPTZ', 'NUMERIC'
  created_at      TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(form_id, field_key)
);

-- TABLE 3: File Upload fields — store S3/MinIO URLs here
-- (response tables store the upload_id; actual metadata here)
CREATE TABLE form_file_uploads (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  form_id         UUID REFERENCES forms(id),
  response_row_id UUID NOT NULL,         -- UUID of the row in the dynamic response table
  field_key       TEXT NOT NULL,
  original_name   TEXT NOT NULL,
  s3_key          TEXT NOT NULL,         -- path in MinIO/S3
  s3_url          TEXT NOT NULL,         -- presigned or public URL
  file_size_bytes INTEGER,
  mime_type       TEXT,
  uploaded_at     TIMESTAMPTZ DEFAULT NOW()
);
```

> **How response tables are created:** When a form is published, the backend runs a DDL `CREATE TABLE` statement. The table name is `form_responses_<uuid_short>`. Each field in `form_fields` becomes a column. File upload fields store a `UUID` referencing `form_file_uploads`. See Section 7 for the full logic.

### 4.5 Schema: Hiring Requisition

```sql
CREATE TYPE requisition_status AS ENUM (
  'draft', 'pending_director', 'pending_cos', 'pending_founder',
  'pending_ptc', 'approved', 'rejected', 'cancelled'
);

CREATE TABLE hiring_requisitions (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title               TEXT NOT NULL,
  job_description     TEXT NOT NULL,
  scope_of_work       TEXT NOT NULL,
  department          TEXT,
  status              requisition_status DEFAULT 'draft',
  created_by          UUID REFERENCES users(id),   -- PTC / HR user
  screening_form_id   UUID REFERENCES forms(id),   -- linked dynamic form
  min_rejection_chars JSONB DEFAULT '{}',           -- {"director":50,"cos":50,"founder":100,"ptc":50}
  created_at          TIMESTAMPTZ DEFAULT NOW(),
  updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Junction: supporting tech team members on a requisition
CREATE TABLE requisition_supporting_members (
  requisition_id  UUID REFERENCES hiring_requisitions(id) ON DELETE CASCADE,
  user_id         UUID REFERENCES users(id),
  PRIMARY KEY (requisition_id, user_id)
);

-- Approval chain audit trail
CREATE TYPE approval_stage AS ENUM ('director', 'chief_of_staff', 'founder', 'ptc');
CREATE TYPE approval_decision AS ENUM ('approved', 'rejected');

CREATE TABLE requisition_approvals (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  requisition_id  UUID REFERENCES hiring_requisitions(id) ON DELETE CASCADE,
  stage           approval_stage NOT NULL,
  decision        approval_decision,
  remarks         TEXT,
  decided_by      UUID REFERENCES users(id),
  decided_at      TIMESTAMPTZ,
  notified_at     TIMESTAMPTZ,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.6 Schema: Recruitment Pipeline

```sql
CREATE TYPE hiring_type AS ENUM ('inbound', 'outbound', 'referral');
CREATE TYPE pipeline_status AS ENUM (
  'active', 'hired', 'rejected', 'withdrawn', 'on_hold'
);
CREATE TYPE stage_name AS ENUM (
  'screening', 'fitment_evaluation', 'technical_interview', 'ptc_round', 'founder_round'
);
CREATE TYPE stage_outcome AS ENUM ('approved', 'rejected', 'pending');

CREATE TABLE pipelines (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  candidate_id        UUID REFERENCES candidates(id),
  requisition_id      UUID REFERENCES hiring_requisitions(id),
  hiring_type         hiring_type NOT NULL DEFAULT 'inbound',
  current_stage       stage_name NOT NULL DEFAULT 'screening',
  status              pipeline_status DEFAULT 'active',
  referral_employee_id UUID REFERENCES users(id),  -- if referral
  created_at          TIMESTAMPTZ DEFAULT NOW(),
  updated_at          TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(candidate_id, requisition_id)             -- one pipeline per candidate per role
);

CREATE TABLE stage_history (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pipeline_id     UUID REFERENCES pipelines(id) ON DELETE CASCADE,
  stage           stage_name NOT NULL,
  outcome         stage_outcome DEFAULT 'pending',
  remarks         TEXT,
  actor_id        UUID REFERENCES users(id),
  zoho_booking_id TEXT,                           -- for Technical Interview stage
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Fitment tasks (up to 5 per role / requisition)
CREATE TABLE fitment_tasks (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  requisition_id  UUID REFERENCES hiring_requisitions(id) ON DELETE CASCADE,
  title           TEXT NOT NULL,
  description     TEXT,
  file_url        TEXT,                            -- S3 link to task brief PDF
  is_default      BOOLEAN DEFAULT FALSE,
  is_archived     BOOLEAN DEFAULT FALSE,
  created_by      UUID REFERENCES users(id),
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Candidate task submissions per pipeline
CREATE TABLE candidate_submissions (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pipeline_id     UUID REFERENCES pipelines(id) ON DELETE CASCADE,
  task_id         UUID REFERENCES fitment_tasks(id),
  s3_key          TEXT NOT NULL,
  s3_url          TEXT NOT NULL,
  original_name   TEXT,
  mime_type       TEXT,
  submitted_at    TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.7 Schema: Email Templates

```sql
CREATE TABLE email_templates (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT UNIQUE NOT NULL,      -- e.g. 'fitment_shortlisted', 'final_offer'
  subject     TEXT NOT NULL,
  body_html   TEXT NOT NULL,             -- WYSIWYG HTML with {{placeholders}}
  version     INTEGER DEFAULT 1,
  is_active   BOOLEAN DEFAULT TRUE,
  updated_by  UUID REFERENCES users(id),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE email_template_history (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  template_id     UUID REFERENCES email_templates(id),
  subject         TEXT NOT NULL,
  body_html       TEXT NOT NULL,
  version         INTEGER NOT NULL,
  saved_by        UUID REFERENCES users(id),
  saved_at        TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.8 Schema: Referrals

```sql
CREATE TABLE referrals (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  pipeline_id         UUID REFERENCES pipelines(id) ON DELETE CASCADE,
  referrer_user_id    UUID REFERENCES users(id),
  referrer_employee_id TEXT NOT NULL,
  relationship        TEXT,
  reason              TEXT NOT NULL,             -- "Why do you recommend?"
  created_at          TIMESTAMPTZ DEFAULT NOW()
);
```

### 4.9 System Configuration

```sql
CREATE TABLE system_config (
  key         TEXT PRIMARY KEY,          -- e.g. 'reapply_cooldown_months', 'rejection_min_chars'
  value       JSONB NOT NULL,
  module      TEXT DEFAULT 'ats',
  updated_by  UUID REFERENCES users(id),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Seed defaults:
-- ('reapply_cooldown_months', '3', 'ats')
-- ('rejection_min_chars', '{"screening":50,"fitment":50,"technical":100,"ptc":50,"founder":50}', 'ats')
```

---

## 5. Backend — FastAPI

### 5.1 Project Setup

```bash
# In services/api/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt`:

```
fastapi==0.111.0
uvicorn[standard]==0.29.0
sqlalchemy[asyncio]==2.0.30
asyncpg==0.29.0
alembic==1.13.1
pydantic==2.7.1
pydantic-settings==2.2.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
boto3==1.34.0               # S3 / MinIO
celery[redis]==5.3.6
redis==5.0.4
httpx==0.27.0               # Async HTTP client (Zoho APIs)
jinja2==3.1.4               # Email templates
pytest==8.2.0
pytest-asyncio==0.23.6
```

### 5.2 `app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.admin.router import router as admin_router
from app.modules.ats.forms.router import router as forms_router
from app.modules.ats.requisitions.router import router as req_router
from app.modules.ats.pipeline.router import router as pipeline_router
from app.modules.ats.candidates.router import router as candidate_router
from app.modules.ats.emails.router import router as email_router

app = FastAPI(title="ERP – ATS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with prefix
app.include_router(auth_router,      prefix="/api/v1/auth",        tags=["Auth"])
app.include_router(admin_router,     prefix="/api/v1/admin",       tags=["Admin"])
app.include_router(forms_router,     prefix="/api/v1/forms",       tags=["Forms"])
app.include_router(req_router,       prefix="/api/v1/requisitions", tags=["Requisitions"])
app.include_router(pipeline_router,  prefix="/api/v1/pipelines",   tags=["Pipeline"])
app.include_router(candidate_router, prefix="/api/v1/candidates",  tags=["Candidates"])
app.include_router(email_router,     prefix="/api/v1/email-templates", tags=["Email Templates"])

@app.get("/health")
def health():
    return {"status": "ok"}
```

### 5.3 `app/core/config.py`

```python
from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    REDIS_URL: str = "redis://localhost:6379/0"

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str
    MINIO_USE_SSL: bool = False

    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAIL_FROM_NAME: str = "Aerospace Recruitment"

    ZOHO_CLIENT_ID: str = ""
    ZOHO_CLIENT_SECRET: str = ""
    ZOHO_PEOPLE_API_BASE: str = ""
    ZOHO_BOOKINGS_API_BASE: str = ""

    FRONTEND_URL: str
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"

settings = Settings()
```

### 5.4 `app/core/database.py`

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

### 5.5 `app/core/dependencies.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.auth.service import get_user_by_id

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await get_user_by_id(db, payload["sub"])
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

def require_roles(*roles):
    """Usage: Depends(require_roles('admin', 'ptc'))"""
    async def checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user
    return checker
```

### 5.6 Alembic Migrations

```bash
# Initialize (already done in project setup)
alembic init alembic

# Create a new migration
alembic revision --autogenerate -m "create_ats_tables"

# Run migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

`alembic/env.py` must import all models so autogenerate detects them:

```python
from app.core.database import Base
# Import all model files so SQLAlchemy registers them
import app.modules.ats.forms.models       # noqa
import app.modules.ats.requisitions.models  # noqa
import app.modules.ats.pipeline.models    # noqa
import app.modules.auth.models            # noqa
```

---

## 6. Frontend — React

### 6.1 Project Setup

```bash
cd frontend
npm create vite@latest . -- --template react   # plain JS, NOT react-ts
npm install
npm install react-router-dom @tanstack/react-query zustand axios
npm install -D tailwindcss postcss autoprefixer eslint eslint-plugin-react eslint-plugin-react-hooks
npx tailwindcss init -p
```

> **No TypeScript.** All files use `.jsx` (components) or `.js` (hooks, utils, stores, services).
> Use **JSDoc comments** (`/** @param {string} id */`) on shared utility functions so editors still show
> inline hints without needing a compiler. This is the same approach used by projects like Svelte's
> own codebase and many mid-size teams who want IDE help without the TS build overhead.

### 6.2 Route Structure

```
/                        → redirect to /app/dashboard or /login
/login                   → Staff login (email + password)
/candidate/apply/:formId → Public candidate form (no auth required)
/candidate/portal        → Candidate magic-link portal (track applications)

/app/                    → Protected (all staff roles)
  dashboard              → Role-specific dashboard
  admin/
    users                → User management (Admin only)
    roles                → Role assignment (Admin only)
    config               → System config (Admin, PTC)
  forms/
    builder              → Form builder list (Admin, PTC)
    builder/:formId      → Edit/create form
    responses/:formId    → View form responses
  requisitions/
    list                 → All requisitions
    new                  → Create requisition
    :id                  → Requisition detail + approval
  pipeline/
    :requisitionId       → Kanban / Tabular view
    candidate/:pipelineId → Individual candidate pipeline view
  email-templates/       → Template editor (Admin, PTC)
```

### 6.3 Auth State (Zustand)

```javascript
// src/store/authStore.js
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

// Shape: { user: { id, email, fullName, role } | null, accessToken: string | null }
export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      setAuth: (user, accessToken) => set({ user, accessToken }),
      logout: () => set({ user: null, accessToken: null }),
    }),
    { name: 'erp-auth' }
  )
)
```

### 6.4 API Client

```javascript
// src/lib/apiClient.js
import axios from 'axios'
import { useAuthStore } from '@/store/authStore'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
})

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

apiClient.interceptors.response.use(
  (res) => res,
  async (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

### 6.5 Role-Based UI Guard

```jsx
// src/modules/shared/guards/RoleGuard.jsx
import { Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'

// allowedRoles: string[]  e.g. ['admin', 'ptc']
// fallback: optional node to render instead of redirecting
export function RoleGuard({ allowedRoles, children, fallback }) {
  const user = useAuthStore((s) => s.user)
  if (!user) return <Navigate to="/login" />
  if (!allowedRoles.includes(user.role)) {
    return fallback ? fallback : <Navigate to="/app/dashboard" />
  }
  return children
}
```

---

## 7. Dynamic Form Builder

This is the most complex feature. Read carefully.

### 7.1 How It Works (End-to-End)

```
Admin/PTC → Form Builder UI (drag & drop fields)
         → POST /api/v1/forms           (saves to 'forms' + 'form_fields' tables)
         → On Publish: backend runs DDL
           CREATE TABLE form_responses_<uuid> (
             id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
             submitted_at TIMESTAMPTZ DEFAULT NOW(),
             candidate_id UUID,          -- nullable for anonymous
             <field_key_1> TEXT,
             <field_key_2> INTEGER,
             ...
           )
         → Form URL shared: /candidate/apply/:formId
         → Candidate fills form → POST /api/v1/forms/:formId/submit
         → Backend inserts into form_responses_<uuid>
         → File fields: upload to MinIO → store URL in form_file_uploads
                        store file_upload_id UUID in response table column
```

### 7.2 Backend: Form Creation API

```python
# app/modules/ats/forms/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import require_roles
from . import schemas, service

router = APIRouter()

@router.post("/", response_model=schemas.FormOut)
async def create_form(
    payload: schemas.FormCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles("admin", "ptc"))
):
    return await service.create_form(db, payload, current_user.id)

@router.post("/{form_id}/publish")
async def publish_form(
    form_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles("admin", "ptc"))
):
    """Creates the dynamic response table in PostgreSQL."""
    return await service.publish_form(db, form_id)

@router.post("/{form_id}/submit")
async def submit_form(
    form_id: str,
    payload: dict,                         # dynamic — validated against form_fields
    db: AsyncSession = Depends(get_db)
):
    """Public endpoint — no auth required for candidates."""
    return await service.submit_form(db, form_id, payload)

@router.get("/{form_id}/responses")
async def get_responses(
    form_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(require_roles("admin", "ptc"))
):
    return await service.get_form_responses(db, form_id)
```

### 7.3 Backend: DDL Table Creation Logic

```python
# app/modules/ats/forms/service.py  (partial)
import uuid
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# Map field_type → PostgreSQL column type
FIELD_TYPE_MAP = {
    "text":         "TEXT",
    "textarea":     "TEXT",
    "email":        "TEXT",
    "number":       "NUMERIC",
    "date":         "DATE",
    "select":       "TEXT",
    "multi_select": "TEXT[]",
    "checkbox":     "BOOLEAN",
    "radio":        "TEXT",
    "file_upload":  "UUID",             # stores ID from form_file_uploads
    "section_header": None,            # not a real column, skip
}

async def publish_form(db: AsyncSession, form_id: str):
    # 1. Fetch form and fields
    form = await db.get(Form, form_id)
    if form.response_table:
        raise ValueError("Form already published")

    fields = await get_fields_for_form(db, form_id)

    # 2. Generate safe table name
    short_id = str(uuid.uuid4()).replace("-", "")[:12]
    table_name = f"form_responses_{short_id}"

    # 3. Build column definitions
    col_defs = [
        "id UUID PRIMARY KEY DEFAULT gen_random_uuid()",
        "submitted_at TIMESTAMPTZ DEFAULT NOW()",
        "candidate_id UUID",
        "ip_address TEXT",
    ]
    for field in fields:
        pg_type = FIELD_TYPE_MAP.get(field.field_type)
        if pg_type is None:
            continue                   # skip section_header
        safe_key = field.field_key.replace(" ", "_").lower()
        col_defs.append(f'"{safe_key}" {pg_type}')

    # 4. Execute DDL
    ddl = f"CREATE TABLE {table_name} ({', '.join(col_defs)});"
    await db.execute(text(ddl))

    # 5. Save table name back to forms table
    form.response_table = table_name
    await db.commit()
    return {"table_created": table_name}

async def submit_form(db: AsyncSession, form_id: str, payload: dict):
    form = await db.get(Form, form_id)
    fields = {f.field_key: f for f in await get_fields_for_form(db, form_id)}

    # Validate required fields
    for key, field in fields.items():
        if field.is_required and key not in payload:
            raise ValueError(f"Field '{field.label}' is required")

    # Build INSERT
    columns = ["candidate_id"]
    values = [payload.get("candidate_id")]

    for key, field in fields.items():
        if FIELD_TYPE_MAP.get(field.field_type) is None:
            continue
        columns.append(f'"{key}"')
        values.append(payload.get(key))

    placeholders = ", ".join([f":{i}" for i in range(len(values))])
    col_str = ", ".join(columns)

    insert_sql = text(
        f"INSERT INTO {form.response_table} ({col_str}) "
        f"VALUES ({placeholders}) RETURNING id"
    )
    result = await db.execute(insert_sql, dict(enumerate(values)))
    await db.commit()
    return {"response_id": result.scalar()}
```

### 7.4 Frontend: Form Builder UI

The Form Builder is a drag-and-drop interface similar to Google Forms.

**Component breakdown:**

```
FormBuilder/
  FormBuilderPage.jsx         # Main page — left sidebar + preview
  FieldPalette.jsx            # Left sidebar: draggable field types
  FieldList.jsx               # Center: current fields, reorderable
  FieldEditor.jsx             # Right panel: edit selected field props
  FieldPreview.jsx            # What the filled form looks like
  PublishButton.jsx           # Calls /forms/:id/publish
```

**Field types to support in the UI:**

| Type | Label | Notes |
|---|---|---|
| `text` | Short Text | Single line |
| `textarea` | Long Text | Multi-line |
| `email` | Email | With format validation |
| `number` | Number | Min/max validation |
| `date` | Date Picker | |
| `select` | Dropdown | Add options list |
| `multi_select` | Multi-Select | Checkboxes list |
| `radio` | Radio Group | Single choice |
| `checkbox` | Single Checkbox | Yes/No |
| `file_upload` | File Upload | Accept: PDF, ZIP (configurable) |
| `section_header` | Section Header | Visual separator, no DB column |

**Form submission (candidate side):**

```javascript
// Dynamically render fields from API response
const { data: formData } = useQuery({
  queryKey: ['form', formId],
  queryFn: () => apiClient.get(`/forms/${formId}/public`).then(r => r.data)
})

// formData.fields is an array of form_fields rows
// Render each field based on field_type
```

### 7.5 File Upload in Forms

1. When a candidate selects a file for a `file_upload` field, the frontend calls:
   `POST /api/v1/uploads/presigned-url` with `{ filename, content_type, form_id, field_key }`.
2. Backend generates a presigned PUT URL from MinIO and returns it.
3. Frontend uploads the file directly to MinIO using the presigned URL.
4. Frontend then submits the form payload with `{ field_key: upload_reference_id }`.
5. Backend links the upload record to the form response row.

---

## 8. Authentication & RBAC

### 8.1 Staff Authentication Flow

```
1. Admin creates user (POST /admin/users) → email sent with OTP
2. User visits /register?token=<otp> → sets password
3. Login: POST /auth/login { email, password }
   → Returns { access_token, refresh_token }
4. Refresh: POST /auth/refresh { refresh_token }
   → Returns new access_token
```

### 8.2 Candidate Authentication (Magic Link)

```
1. Candidate visits /candidate/apply/:formId → fills form (no auth needed)
   OR
   Candidate visits /candidate/portal → enters email
2. POST /auth/candidate/send-otp { email }
   → Backend sends 6-digit OTP to email (stored in Redis, 10 min TTL)
3. POST /auth/candidate/verify-otp { email, otp }
   → Returns short-lived JWT (15 min session)
4. Candidate JWT has role: 'candidate' + candidate_id claim
```

### 8.3 Role Permissions Matrix (Enforce in Backend)

Every protected route uses `Depends(require_roles(...))`.

| Endpoint Group | Allowed Roles |
|---|---|
| `GET /pipelines` (all) | admin, founder, project_director, ptc |
| `GET /pipelines` (own requisitions) | hiring_manager |
| `POST /requisitions` | ptc |
| `POST /requisitions/:id/approve` | director, chief_of_staff, founder, ptc |
| `POST /pipeline/:id/stage` (screening) | ptc |
| `POST /pipeline/:id/stage` (fitment, technical) | hiring_manager |
| `POST /pipeline/:id/stage` (ptc_round) | ptc |
| `POST /pipeline/:id/stage` (founder_round) | founder |
| `GET/PUT /email-templates` | admin, ptc |
| `GET/PUT /system-config` | admin, ptc |
| `POST /admin/users` | admin |
| `GET /forms` | admin, ptc |
| `POST /forms` | admin, ptc |
| `POST /forms/:id/submit` | public (no auth) |
| `GET /forms/:id/responses` | admin, ptc |

### 8.4 JWT Structure

```json
// Access token payload
{
  "sub": "user-uuid",
  "email": "user@company.com",
  "role": "ptc",
  "type": "access",
  "exp": 1234567890
}
```

```python
# app/core/security.py
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": user_id, "role": role, "type": "access", "exp": expire},
        settings.SECRET_KEY, algorithm="HS256"
    )

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        return None
```

### 8.5 Admin UI: User Management

Admin sees a Users page (`/app/admin/users`) with:

- Table of all users (name, email, role, department, active/inactive, created date).
- "Invite User" button → modal with: email, full name, role dropdown (all roles except Admin), department.
- On submit: backend creates user + sends OTP email for them to set password.
- Toggle active/inactive per user.
- Edit role (cannot edit own role).

---

## 9. File Storage

### 9.1 MinIO (S3-compatible)

All files (CVs, task submissions, form uploads) go to MinIO. The database **never** stores binary data — only S3 keys and URLs.

**S3 Key Conventions:**

```
ats/cvs/<candidate_id>/<uuid>/<original_filename>
ats/submissions/<pipeline_id>/<uuid>/<original_filename>
ats/forms/<form_id>/<response_row_id>/<field_key>/<uuid>/<original_filename>
ats/fitment-tasks/<task_id>/<uuid>/<original_filename>
```

**Backend S3 helper (`app/core/storage.py`):**

```python
import boto3
from botocore.client import Config
from app.core.config import settings

def get_s3_client():
    return boto3.client(
        "s3",
        endpoint_url=f"http{'s' if settings.MINIO_USE_SSL else ''}://{settings.MINIO_ENDPOINT}",
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
    )

def generate_presigned_put(s3_key: str, content_type: str, expires: int = 300) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.MINIO_BUCKET_NAME, "Key": s3_key, "ContentType": content_type},
        ExpiresIn=expires,
    )

def generate_presigned_get(s3_key: str, expires: int = 3600) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.MINIO_BUCKET_NAME, "Key": s3_key},
        ExpiresIn=expires,
    )
```

**File type and size validation (backend):**

```python
ALLOWED_CV_TYPES = {"application/pdf"}
ALLOWED_SUBMISSION_TYPES = {"application/pdf", "application/zip", "application/x-zip-compressed"}
MAX_FILE_SIZE_MB = 50

def validate_upload(filename: str, content_type: str, size_bytes: int, allowed_types: set):
    if content_type not in allowed_types:
        raise ValueError(f"File type not allowed: {content_type}")
    if size_bytes > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError(f"File exceeds {MAX_FILE_SIZE_MB}MB limit")
```

---

## 10. Email System

### 10.1 Architecture

Emails are sent **asynchronously** via Celery + Redis. The FastAPI app enqueues a task; the Celery worker processes it and sends via SMTP.

```
FastAPI endpoint → celery.send_task('email_tasks.send_email', args=[...]) → Redis queue
                                                  ↓
                                     Celery Worker pulls task
                                                  ↓
                                     Renders Jinja2 template
                                                  ↓
                                     Sends via SMTP
```

### 10.2 Email Triggers

| Event | Template | Recipients |
|---|---|---|
| Screening shortlisted (internal) | `screening_shortlisted` | Hiring Manager, Supporting Team, careers@ |
| Fitment shortlisted | `fitment_shortlisted` | Candidate |
| Fitment rejected | `fitment_rejected` | Candidate |
| Technical shortlisted | `technical_shortlisted` | Candidate |
| Technical rejected | `technical_rejected` | Candidate |
| PTC shortlisted | `ptc_shortlisted` | Candidate |
| PTC rejected | `ptc_rejected` | Candidate |
| Founder shortlisted | `founder_shortlisted` | Candidate |
| Founder rejected | `founder_rejected` | Candidate |
| Final offer | `final_offer` | Candidate |
| Requisition rejected | `requisition_rejected` | Requisition creator (PTC) |
| Referral hired | `referral_hired` | Referrer employee |

**Note:** Screening stage (Stage 1) does **NOT** send email to candidate. First candidate email is at Fitment Evaluation (Stage 2).

### 10.3 Template Variables

Templates (stored in `email_templates` table as HTML) use `{{ placeholder }}` syntax:

```
{{candidate_name}}       {{role}}              {{department}}
{{company_name}}         {{interview_link}}    {{interview_date}}
{{hiring_manager_name}}  {{rejection_reason}}  {{offer_details}}
{{reapply_date}}
```

### 10.4 Celery Task

```python
# app/workers/tasks/email_tasks.py
from app.workers.celery_app import celery_app
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

@celery_app.task(name="email_tasks.send_email", bind=True, max_retries=3)
def send_email(self, to: list[str], subject: str, body_html: str, context: dict):
    try:
        template = Template(body_html)
        rendered = template.render(**context)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.SMTP_USER}>"
        msg["To"] = ", ".join(to)
        msg.attach(MIMEText(rendered, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, to, msg.as_string())
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
```

---

## 11. Docker & Infrastructure

### 11.1 `infra/docker-compose.yml` (Development)

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  minio:
    image: minio/minio:latest
    restart: unless-stopped
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ACCESS_KEY}
      MINIO_ROOT_PASSWORD: ${MINIO_SECRET_KEY}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"    # MinIO console UI

  api:
    build:
      context: ../services/api
      dockerfile: Dockerfile
    restart: unless-stopped
    env_file: ../.env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    ports:
      - "8000:8000"
    volumes:
      - ../services/api:/app    # Hot reload in dev
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  celery_worker:
    build:
      context: ../services/api
      dockerfile: Dockerfile
    restart: unless-stopped
    env_file: ../.env
    depends_on:
      - redis
      - postgres
    command: celery -A app.workers.celery_app worker --loglevel=info

  web:
    build:
      context: ../apps/web
      dockerfile: Dockerfile
    restart: unless-stopped
    ports:
      - "5173:5173"
    volumes:
      - ../apps/web:/app
      - /app/node_modules
    command: npm run dev -- --host

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

### 11.2 `services/api/Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 11.3 `apps/web/Dockerfile`

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
```

### 11.4 Running the Project

```bash
# 1. Clone and setup env
git clone <repo>
cd erp-aerospace
cp .env.example .env
# Edit .env with real values

# 2. Start all services
cd infra
docker compose up -d

# 3. Run DB migrations
docker compose exec api alembic upgrade head

# 4. Seed initial admin
docker compose exec api python scripts/seed_db.py

# 5. Access
# Frontend:    http://localhost:5173
# Backend API: http://localhost:8000/docs
# MinIO UI:    http://localhost:9001
```

---

## 12. API Reference Summary

### Auth

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/auth/login` | None | Staff login (email + password) |
| POST | `/auth/refresh` | None | Refresh access token |
| POST | `/auth/logout` | Staff | Revoke refresh token |
| POST | `/auth/candidate/send-otp` | None | Send OTP to candidate email |
| POST | `/auth/candidate/verify-otp` | None | Verify OTP, get JWT |

### Admin

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/admin/users` | Admin | List all users |
| POST | `/admin/users` | Admin | Invite/create user |
| PUT | `/admin/users/:id` | Admin | Update user (role, active) |
| GET | `/admin/config` | Admin, PTC | Get system config |
| PUT | `/admin/config` | Admin, PTC | Update config values |

### Forms

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/forms` | Admin, PTC | List all forms |
| POST | `/forms` | Admin, PTC | Create form |
| GET | `/forms/:id` | Admin, PTC | Get form with fields |
| PUT | `/forms/:id` | Admin, PTC | Update form metadata/fields |
| POST | `/forms/:id/publish` | Admin, PTC | Publish form (creates response table) |
| GET | `/forms/:id/public` | None | Get form for candidate filling |
| POST | `/forms/:id/submit` | None | Submit form response |
| GET | `/forms/:id/responses` | Admin, PTC | Get all responses (from dynamic table) |
| POST | `/uploads/presigned-url` | None | Get presigned URL for file upload |

### Requisitions

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/requisitions` | Admin, PTC, Director, Founder | List requisitions |
| POST | `/requisitions` | PTC | Create requisition |
| GET | `/requisitions/:id` | Role-based | Get requisition detail |
| POST | `/requisitions/:id/approve` | Director/CoS/Founder/PTC | Approve/reject stage |

### Pipeline

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/pipelines` | Role-based | List pipelines (filtered by role) |
| POST | `/pipelines` | PTC | Create pipeline (outbound/referral) |
| GET | `/pipelines/:id` | Role-based | Get pipeline detail |
| POST | `/pipelines/:id/stage` | Stage owner | Advance/reject stage |
| GET | `/pipelines/kanban/:requisitionId` | Role-based | Kanban view data |

### Email Templates

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/email-templates` | Admin, PTC | List all templates |
| GET | `/email-templates/:name` | Admin, PTC | Get single template |
| PUT | `/email-templates/:name` | Admin, PTC | Update template |
| GET | `/email-templates/:name/history` | Admin, PTC | Get version history |

---

## 13. Environment Variables

Full list with descriptions for `.env.example`:

```env
# ─── PostgreSQL ───────────────────────────────────────
POSTGRES_USER=erp_user
POSTGRES_PASSWORD=changeme_strong_password
POSTGRES_DB=erp_db
POSTGRES_HOST=postgres          # service name in docker-compose
POSTGRES_PORT=5432

# ─── Redis ────────────────────────────────────────────
REDIS_URL=redis://redis:6379/0

# ─── Security ─────────────────────────────────────────
# Generate with: openssl rand -hex 32
SECRET_KEY=replace_with_256bit_random_hex
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# ─── File Storage (MinIO / S3) ────────────────────────
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin_secret
MINIO_BUCKET_NAME=erp-files
MINIO_USE_SSL=false
# For production AWS S3, change endpoint and set USE_SSL=true

# ─── Email / SMTP ─────────────────────────────────────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=noreply@yourcompany.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM_NAME=Aerospace Careers

# ─── Zoho Integrations ────────────────────────────────
ZOHO_CLIENT_ID=
ZOHO_CLIENT_SECRET=
ZOHO_PEOPLE_API_BASE=https://people.zoho.com/api/v2
ZOHO_BOOKINGS_API_BASE=https://bookings.zoho.com/api/v1
# Zoho OAuth tokens are stored in DB after initial auth flow

# ─── App ──────────────────────────────────────────────
APP_ENV=development             # 'development' | 'production'
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
CORS_ORIGINS=["http://localhost:5173"]

# ─── Celery ───────────────────────────────────────────
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

---

## 14. README Template

Create `erp-aerospace/README.md`:

```markdown
# ERP Aerospace Platform

Internal ERP system for [Company Name]. Modular architecture — current modules: **ATS** (Applicant Tracking System).

## Modules

| Module | Status | Description |
|---|---|---|
| ATS | 🚧 In Development | Applicant Tracking System |
| Inventory | 📋 Planned | - |
| Finance | 📋 Planned | - |

## Tech Stack

- **Frontend**: React 18, Vite, Tailwind CSS, TanStack Query
- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2 (async)
- **Database**: PostgreSQL 16
- **Cache/Queue**: Redis 7 + Celery
- **File Storage**: MinIO (S3-compatible)
- **Container**: Docker + Docker Compose

## Quick Start (Development)

### Prerequisites
- Docker Desktop installed and running
- Git

### Steps

```bash
git clone <repo-url>
cd erp-aerospace
cp .env.example .env
# Open .env and fill in your values (SECRET_KEY, SMTP credentials, etc.)

cd infra
docker compose up -d

# Wait ~30 seconds for services to start, then:
docker compose exec backend alembic upgrade head
docker compose exec backend python scripts/seed_db.py
docker compose exec backend python scripts/create_minio_bucket.py
```

### Access

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API Docs | http://localhost:8000/docs |
| MinIO Storage UI | http://localhost:9001 |

### Default Admin Credentials
Printed to console after running `seed_db.py`. Change immediately after first login.

## Project Structure

```
erp-aerospace/
├── frontend/    ← React app (Vite + JavaScript + Tailwind)
├── backend/     ← FastAPI app (Python + SQLAlchemy + Celery)
├── infra/       ← Docker Compose, Nginx configs
└── docs/        ← TRD/SRS, BRD, diagrams
```

See `docs/ATS_TRD_SRS.md` for the complete annotated folder tree.

## Running Tests

```bash
# Backend tests
docker compose exec backend pytest tests/ -v

# Frontend lint check
docker compose exec frontend npx eslint src/
```

## Migrations

```bash
# Create new migration after changing a SQLAlchemy model
docker compose exec backend alembic revision --autogenerate -m "describe_your_change"

# Apply all pending migrations
docker compose exec backend alembic upgrade head

# Rollback one migration
docker compose exec backend alembic downgrade -1
```

## Adding a New ERP Module

1. **Backend**: Create `backend/app/modules/<module_name>/` with `router.py`, `service.py`, `schemas.py`, `models.py`. Register router in `backend/app/main.py`.
2. **Frontend**: Create `frontend/src/modules/<module_name>/` with `pages/`, `components/`, `hooks/`, `services/`, `constants/`. Add routes in `frontend/src/routes/`.
3. **DB**: Add models, run `alembic revision --autogenerate`.

## Contributing

1. Branch from `develop`: `git checkout -b feature/your-feature`
2. Follow commit convention: `feat(module): description`
3. Open PR against `develop`

## Documentation

- Business Requirements: `docs/BRD_ATS.html`
- Technical SRS (this guide): `docs/ATS_TRD_SRS.md`
```

---

## Appendix: Key Business Rules (Quick Reference for Devs)

### Pipeline Rules

1. **Inbound / Outbound**: Start at Stage 1 (Screening).
2. **Referral**: Start at Stage 2 (Fitment). PTC can skip Stage 2 with reason.
3. **Rejection at any stage**: Pipeline status → `rejected`. No further stage transitions allowed.
4. **Candidate email**: Sent from Stage 2 onwards only. Stage 1 rejection = silent (no email to candidate).
5. **Reapply cooldown**: Configurable (default 3 months). Enforced by checking `pipelines` table for same `candidate_id + requisition_id` within cooldown window.
6. **Same department, multiple roles**: Candidate shares one Fitment Evaluation task. Separate pipelines after that.

### Requisition Approval Chain

```
Draft
  └→ Project Director (any one approves) → notifies all directors
      └→ Chief of Staff
          └→ Founder (any one approves) → notifies all founders
              └→ PTC (final)
                  └→ Active Hiring + Job Posting auto-created
Rejection at any stage → notify requisition creator (PTC who created it)
```

### Rejection Remarks

Minimum character count is configurable per stage via `system_config`. Backend must validate before recording rejection. Frontend shows character count UI.

### Supporting Members

PTC selects supporting team members per candidate (not per requisition) using Zoho People API data. They receive internal stage emails but have no system login for pipeline access.

---

*Document prepared for junior developer onboarding. For business context, refer to `docs/BRD_ATS.html`. For questions, contact the Systems Architect.*
