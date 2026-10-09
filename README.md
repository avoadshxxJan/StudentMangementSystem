# EduTrack — Smart College Student Management System

> **Department-Wise Student Information and Academic Progress Monitoring System**  
> *Built with Python 3.12, Django 5.1, PostgreSQL/SQLite, Bootstrap 5.3, and Chart.js.*

---

## 1. Project Overview

**EduTrack** is an institutional college management web platform designed to solve a core problem in higher education record-keeping: **maintaining a single, permanent student identity across all academic years while isolating department-specific data and preserving complete historical marks, attendance, and achievements.**

### Core Pillars
- **Permanent Student Identity**: When a student advances to Year 2 or Year 3, previous records are never overwritten. Historical marks and attendance remain intact.
- **Department-Level Isolation**: Head of Departments (HODs) and Faculty access only their authorized departments, courses, and classes.
- **Server-Side Role-Based Access Control (RBAC)**: Supports 8 distinct roles: Super Admin, College Admin, Principal, HOD, Faculty, Class Advisor, Student, and Parent/Guardian.
- **Academic Progress Visualization**: Multi-year comparative trends powered by Chart.js.
- **Beginner-Friendly Architecture**: Structured, clean Django monolith ready for local development (SQLite) or production deployment (PostgreSQL).

---

## 2. Quick Start Guide (Windows PowerShell)

Follow these exact steps to launch EduTrack locally:

### Step 1: Open PowerShell in Project Directory
```powershell
cd C:\Users\avoad\Downloads\studentmanagement
```

### Step 2: Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```
*(If you see an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

### Step 3: Run Database Migrations
```powershell
python manage.py migrate
```

### Step 4: Create Local Development Administrator
```powershell
python manage.py setup_dev_admin
```
*(Creates initial user `admin` with password `Admin@12345EduTrack`)*

### Step 5: Start the Development Web Server
```powershell
python manage.py runserver
```

Open your browser and navigate to:
- **Landing Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Administrative Portal**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 3. Running Automated Tests

To run the automated test suite verifying architecture, role properties, and views:

```powershell
python manage.py test accounts
```

---

## 4. Environment Variables (`.env`)

Configuration is managed via `.env` (loaded automatically by `python-dotenv`):

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Cryptographic signing key | Pre-configured for dev |
| `DEBUG` | Enable debug error traces | `True` for dev |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |
| `DB_ENGINE` | Database type: `sqlite` or `postgresql` | `sqlite` |
| `DB_NAME` | Database file or PostgreSQL DB name | `db.sqlite3` |
| `GEMINI_API_KEY` | (Optional) API key for AI summaries | *Optional* |

---

## 5. Phased Roadmap Progress

- [x] **Phase 1: Project Setup & Architecture** (Completed)
  - Custom User model (`accounts.User`) with 8 institutional roles.
  - `.env` configuration, static and media directories.
  - Bootstrap 5.3 + Chart.js base layout and landing page.
  - Automated tests passing (4/4).
- [ ] **Phase 2: Database Models & Migrations** (Next)
  - Departments, Courses, Academic Years, Semesters, Subjects, Students, Enrollments, Marks, and Attendance models.
- [ ] **Phase 3: Authentication & Role-Based Landing Dashboards**
- [ ] **Phase 4: Departments, Courses & Student Profile Management**
- [ ] **Phase 5: Academic Calendar & Yearly Promotion Workflows**
- [ ] **Phase 6: Attendance & Examination Mark Entry**
- [ ] **Phase 7: Multi-Year Academic Progress Comparison Dashboard**
- [ ] **Phase 8: Skills, Achievement Verification & Faculty Mentoring**
- [ ] **Phase 9: Guardian & Student Self-Service Portals**
- [ ] **Phase 10: Server-Side PDF Report Generation (ReportLab)**
- [ ] **Phase 11: Rule-Based & Optional Gemini AI Progress Insights**
- [ ] **Phase 12: Production Hardening, Audit Logs & Deployment Guide**
