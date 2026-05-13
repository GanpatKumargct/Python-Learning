# Enterprise ERP Architecture & Auth Migration Plan

This document outlines the strategy for restructuring the application into an Enterprise-grade ERP architecture, specifically tailored for aerospace standards, including the implementation of Zoho SSO and Magic Link authentication.

## 1. Authentication Strategy (Dual Flow)

To meet enterprise security standards while maintaining a seamless experience for candidates, we will implement a dual-flow authentication system.

### A. Internal Team Members (ZOHO SSO)
**Target Users:** Admin, PTC Members, Employees.
**Method:** Zoho OAuth 2.0 (OpenID Connect) or SAML 2.0.

**How it works & Keys Needed:**
To integrate Zoho SSO, we act as a Service Provider. The recommended modern approach is **OAuth 2.0 (OIDC)**.
*   **Keys Needed from Zoho Admin Console:**
    1.  `CLIENT_ID`: Identifies our application to Zoho.
    2.  `CLIENT_SECRET`: Authenticates our application to Zoho (must be kept secure in backend `.env`).
    3.  `AUTHORIZED_REDIRECT_URI`: The FastAPI endpoint where Zoho sends the user after successful login (e.g., `https://api.domain.com/auth/zoho/callback`).
*   **Workflow:**
    1. Employee clicks "Login with Zoho".
    2. Frontend redirects to Zoho's login page.
    3. After successful login, Zoho redirects back to our FastAPI backend with an authorization code.
    4. Backend exchanges the code for an Access Token and fetches the user's details (Email, Role) from Zoho.
    5. Backend checks if the user exists in our DB, issues our internal JWT session token, and redirects to the frontend dashboard.

### B. External Candidates (Magic Link / OTP)
**Target Users:** Candidates applying for jobs.
**Method:** Passwordless Magic Link via Email.

*   **Workflow:**
    1. Candidate enters their email on the login/apply page.
    2. Backend generates a highly secure, short-lived (e.g., 15 minutes) JWT or OTP.
    3. Backend sends an email containing a Magic Link (e.g., `https://domain.com/verify?token=XYZ`).
    4. Candidate clicks the link.
    5. Frontend extracts the token, sends it to the backend for validation.
    6. Backend validates, logs the candidate in, and issues a standard session JWT.

---

## 2. Directory Restructuring (Domain-Driven Design)

To scale this as an ERP, we must decouple generic modules from ATS-specific logic. We will introduce a `shared` directory for core infrastructure that any future ERP module (Inventory, CRM, HRIS) can consume.

### Proposed Backend Architecture

```text
app/
├── core/                   # Global settings, DB config, security utils
├── shared/                 # 🚀 REUSABLE ERP MODULES (New)
│   ├── auth/               # Zoho SSO, Magic Links, JWT handling, RBAC
│   ├── forms/              # Dynamic Form Builder engine (reusable across ERP)
│   ├── workflow_engine/    # Generic state-machine (approvals, pipelines)
│   ├── emails/             # Global notification and email templating
│   └── audit/              # Enterprise Audit Logging (tracking who did what)
├── modules/
│   ├── ats/                # 🏢 ATS SPECIFIC BUSINESS LOGIC
│   │   ├── candidates/     # Candidate profiles, resumes
│   │   ├── requisitions/   # Job postings
│   │   ├── referrals/      # Employee referral logic
│   │   ├── pipeline/       # ATS specific pipeline definitions
│   │   ├── dashboards/     # Admin and PTC dashboards for ATS metrics
│   │   └── admin_actions/  # User management and approvals specific to ATS
│   └── other_module/       # Future ERP modules
└── main.py
```

---

## 3. Aerospace ERP Standard Practices

Building for the aerospace sector requires rigorous compliance, reliability, and security. We will enforce the following standards:

1.  **Strict Audit Logging:** Every write/update/delete action (especially in ATS and Auth) must be logged in an `audit_logs` table. We need to know *who* changed *what* and *when*.
2.  **Role-Based Access Control (RBAC):** Centralized in the `shared/auth` module. Endpoints will use strict FastAPI dependencies (e.g., `Depends(require_role(["Admin", "PTC"]))`) to prevent unauthorized access.
3.  **Idempotency:** Critical API endpoints (like generating Magic Links or submitting applications) will use Idempotency Keys to prevent duplicate processing if a user double-clicks.
4.  **Data Isolation:** Candidates can only read/write their own data. Internal users' access is strictly scoped by their Zoho-assigned roles.
5.  **Fault Tolerance:** The `shared/emails` module will use background tasks (Celery or FastAPI `BackgroundTasks`) with retry mechanisms to ensure notifications are never lost.

## 4. Next Steps & Implementation Phases

If you approve this plan, we will execute it in the following phases:

*   **Phase 1: Folder Restructuring:** Move `auth`, `forms`, and `emails` into the `shared` folder. Clean up imports across the application.
*   **Phase 2: Candidate Magic Link Auth:** Implement the passwordless email link flow for external users.
*   **Phase 3: Zoho SSO Integration:** Set up the OAuth2 flow in the backend and frontend for internal team members.
*   **Phase 4: ATS Cleanup:** Ensure the `ats` module strictly relies on the new `shared` infrastructure.

Please review this plan. If it aligns with your vision, let me know, and we will begin Phase 1 immediately!
