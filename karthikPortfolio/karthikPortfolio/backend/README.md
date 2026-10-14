# Karthik Portfolio — FastAPI Backend & Database Service

A secure, high-performance Python backend built with **FastAPI**, **SQLAlchemy 2.x**, **SQLite**, and **SMTP email delivery** to handle contact inquiries, store messages persistently, and dispatch email alerts for Karthik Venkata Jaya Karthik's developer portfolio.

---

## 🌟 Architecture & Features

- **Framework**: FastAPI (asynchronous, high throughput, auto-generated interactive OpenAPI docs).
- **ORM & Database**: SQLAlchemy 2.x with SQLite for zero-configuration local persistence (`backend/portfolio.db`). Seamlessly configurable for PostgreSQL in production.
- **Data Validation**: Pydantic v2 schemas enforcing required fields, email formatting, string trimming, and boundaries.
- **Email Delivery**: SMTP transport with HTML & plain-text templates, reply-to routing, and timeouts. Safe fallback if unconfigured.
- **Abuse Prevention**:
  - Sliding-window in-memory rate limiting (max 5 requests per 10 minutes per IP).
  - Anti-spam honeypot detection (`_gotcha` / `honeypot`).
  - Request body size limits (max 64 KB).
- **Security**: CORS restricted to configured frontend origins, safe error handling without leaking stack traces or passwords.
- **Testing**: 20 automated tests with pytest, httpx, in-memory SQLite, and email service mocking.

---

## 📋 Prerequisites

- **Python 3.10+** (Python 3.12 verified)
- **Windows Command Prompt (CMD)** or **PowerShell**

---

## 🚀 Quick Start Guide (Windows CMD)

Follow these exact step-by-step commands in your Windows Command Prompt:

### 1. Open the Project Folder

```cmd
cd "c:\Users\KOSANA SURYA\OneDrive\Desktop\karthikPortfolio\backend"
```

### 2. Create a Python Virtual Environment

```cmd
python -m venv venv
```

### 3. Activate the Virtual Environment

In Windows Command Prompt (CMD):
```cmd
venv\Scripts\activate
```

*(If using PowerShell: `.\venv\Scripts\Activate.ps1`)*

### 4. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create your local `.env` configuration file from the template:

```cmd
copy .env.example .env
```

Open `.env` in Notepad or VS Code:
```cmd
notepad .env
```

#### Key Variables in `.env`:
- `DATABASE_URL`: `sqlite:///./portfolio.db` (persists messages in `backend/portfolio.db`)
- `FRONTEND_ORIGINS`: Comma-separated allowed URLs (e.g. `http://127.0.0.1:5500,http://localhost:5500,http://127.0.0.1:8000`)
- `SMTP_HOST`: (Optional) e.g. `smtp.gmail.com`
- `SMTP_PORT`: `587`
- `SMTP_USERNAME`: Your email address
- `SMTP_PASSWORD`: Your 16-character App Password (for Gmail: Google Account > Security > App Passwords)
- `SENDER_EMAIL`: Your verified sender address
- `RECIPIENT_EMAIL`: `karanamvenkatjaykarthik@gmail.com`

> **Note:** If SMTP credentials are left empty, the backend will still safely save all messages in the database and report that the message was received and stored.

---

## 🏃 Running the Application

### 6. Start the FastAPI Server with Uvicorn

From inside the `backend` directory:
```cmd
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

You will see output indicating the server has started:
```text
INFO:     Started server process
INFO:     Initializing database tables...
INFO:     Database schema initialized successfully.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 7. Interactive API Documentation

Open your web browser and navigate to:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔍 API Verification Commands

You can verify the running server from another Command Prompt window:

### 8. Check Application Health

```cmd
curl http://127.0.0.1:8000/api/health
```
**Expected Response:**
```json
{"status":"healthy","service":"portfolio-backend","timestamp":"2026-10-09T05:30:00Z"}
```

### 9. Check Database Connectivity

```cmd
curl http://127.0.0.1:8000/api/health/db
```
**Expected Response:**
```json
{"status":"healthy","database":"connected","timestamp":"2026-10-09T05:30:00Z"}
```

### 10. Test Contact Form Submission via curl

```cmd
curl -X POST http://127.0.0.1:8000/api/contact ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Recruiter Alex\",\"email\":\"alex@company.com\",\"subject\":\"Engineering Opportunity\",\"message\":\"Hello Karthik, I reviewed your portfolio and would like to connect.\"}"
```

**Expected Response (when SMTP is unconfigured):**
```json
{
  "status": "success",
  "message": "Your message has been received and saved securely in our database. (Server email notification is currently unconfigured).",
  "email_status": "unconfigured",
  "ticket_id": 1
}
```

---

## 🧪 Running Automated Tests

Run the full 20-test automated suite using `pytest`:

From the `backend/` directory:
```cmd
pytest tests -v
```

All 20 tests execute against an isolated in-memory test database with mocked email services:
```text
backend/tests/test_contact.py::test_valid_contact_submission_email_success PASSED
backend/tests/test_contact.py::test_valid_contact_submission_email_failure PASSED
backend/tests/test_contact.py::test_valid_contact_submission_unconfigured_email PASSED
backend/tests/test_contact.py::test_missing_required_fields PASSED
backend/tests/test_contact.py::test_invalid_email_format PASSED
backend/tests/test_contact.py::test_empty_or_whitespace_message PASSED
backend/tests/test_contact.py::test_message_too_short PASSED
backend/tests/test_contact.py::test_overly_long_fields PASSED
backend/tests/test_contact.py::test_malformed_json_request PASSED
backend/tests/test_contact.py::test_honeypot_spam_detected PASSED
backend/tests/test_contact.py::test_rate_limiting PASSED
backend/tests/test_contact.py::test_no_secrets_in_error_responses PASSED
backend/tests/test_database.py::test_create_contact_message PASSED
backend/tests/test_database.py::test_contact_message_persistence PASSED
backend/tests/test_database.py::test_contact_message_email_status_update PASSED
backend/tests/test_database.py::test_contact_message_missing_required_fields PASSED
backend/tests/test_health.py::test_root_status PASSED
backend/tests/test_health.py::test_app_health PASSED
backend/tests/test_health.py::test_db_health PASSED
backend/tests/test_health.py::test_db_health_failure_handled PASSED
======================= 20 passed in 1.40s =======================
```

---

## 🌐 Connecting the Frontend

1. **Start the backend** on port 8000:
   ```cmd
   uvicorn app.main:app --port 8000 --reload
   ```

2. **Serve the frontend** (using VS Code Live Server on port 5500, or Python's built-in static server):
   ```cmd
   cd "c:\Users\KOSANA SURYA\OneDrive\Desktop\karthikPortfolio"
   python -m http.server 5500
   ```

3. Open `http://127.0.0.1:5500/index.html` in your browser.
4. Fill out the **Let's Connect** form and click **Send Message**:
   - The frontend calls `http://127.0.0.1:8000/api/contact`.
   - The message is validated and saved in `portfolio.db`.
   - The frontend displays real confirmation.

---

## 🛑 Stopping the Server

Press `CTRL + C` in the Command Prompt running Uvicorn.

---

## 💾 Database Backup & Restore

### Backup
To create a backup copy of your SQLite database:
```cmd
copy portfolio.db portfolio_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db
```

### Restore
To restore from a backup:
```cmd
copy portfolio_backup_YYYYMMDD.db portfolio.db
```

---

## 🚀 Transitioning to PostgreSQL (Production)

The backend uses standard SQLAlchemy 2.x ORM models without SQLite-specific syntax. To migrate to PostgreSQL in production:
1. Install the PostgreSQL driver:
   ```cmd
   pip install psycopg2-binary
   ```
2. In your production `.env`, set:
   ```env
   DATABASE_URL=postgresql://db_user:db_password@db_host:5432/portfolio_db
   ```
The tables will automatically be created on server startup.
