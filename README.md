# EduTrack — Smart College Student Management System

> **Department-Wise Student Information and Academic Progress Monitoring System**  
> *Phase 1 Foundation: Project Setup, Architecture, Configuration, Custom User Model, and UI Design Tokens.*

---

## 1. Project Overview & Phase 1 Scope

**EduTrack** is an institutional college management web application designed to solve a core problem in higher-education administration: **maintaining a single, permanent student identity across all academic years while isolating departmental records and preserving complete historical marks, attendance, and achievements.**

### Phase 1 Deliverables (Foundation Only)
This phase establishes the foundational project infrastructure and strict architectural conventions:
- **Clean Django Monolith Architecture**: Pinned stable Django 5.1.x on Python 3.12.
- **Custom User Model**: `accounts.User` extending `AbstractUser` with unique email enforcement and 8 institutional roles. Configured **prior** to running any database migrations (`AUTH_USER_MODEL = 'accounts.User'`).
- **Environment-Driven Settings**: Configuration loaded via `python-dotenv` from the root `.env` without hard-coded secrets.
- **Base UI Design System**: Bootstrap 5.3 integration, CSS custom properties (design tokens), accessible HTML5 semantic landmarks, and modular includes (`navbar.html`, `footer.html`, `messages.html`).
- **Informational Landing Page**: `pages/home.html` previewing planned academic modules without displaying fabricated metrics.
- **Automated Test Suite**: 10 unit tests covering custom authentication, role choices, email uniqueness, password hashing, environment loading, and view resolution.

> **Important Scope Notice**: Future modules including department and course CRUD, student enrollment advancement, attendance sessions, exam marks, GPA calculation, parent portals, PDF transcripts, and AI-assisted insights are explicitly scheduled for Phases 2–12.

---

## 2. Technology Stack & Prerequisites

- **Language**: Python 3.12+
- **Backend Framework**: Django 5.1.15 (Pinned LTS/stable monolithic framework)
- **Database**: SQLite (Local development) &bull; PostgreSQL ready (Production)
- **Configuration**: `python-dotenv` 1.0.x
- **Frontend**: Django Templates, HTML5, CSS3 Custom Tokens, Bootstrap 5.3, Vanilla JavaScript
- **Testing**: Django's built-in testing framework (`TestCase`, `Client`)
- **Version Control**: Git

---

## 3. Project Directory Structure

```text
edutrack/
├── manage.py                   # Django CLI management entrypoint
├── requirements.txt            # Pinned package dependencies
├── .env                        # Local development environment configuration (git-ignored)
├── .env.example                # Configuration template with placeholders
├── .gitignore                  # Git exclusion rules for secrets, DB, and media
├── README.md                   # Setup guide, commands, and project status
├── config/                     # Django project configuration package
│   ├── __init__.py
│   ├── settings.py             # Settings reading .env, auth, DB, static/media
│   ├── urls.py                 # Root URL router (/admin/ and /)
│   ├── asgi.py                 # ASGI entrypoint
│   └── wsgi.py                 # WSGI entrypoint
├── accounts/                   # User authentication & institutional role management
│   ├── __init__.py
│   ├── admin.py                # Django Admin integration with UserAdmin
│   ├── apps.py                 # AccountsConfig
│   ├── models.py               # Custom User model & UserRole TextChoices
│   ├── managers.py             # UserManager enforcing email uniqueness
│   ├── tests.py                # 10 automated unit tests
│   ├── migrations/             # Database migrations for accounts
│   │   ├── 0001_initial.py
│   │   └── 0002_alter_user_options_alter_user_managers_and_more.py
│   ├── management/             # Management commands
│   │   └── commands/
│   │       └── setup_dev_admin.py # Idempotent initial admin creation command
│   └── views.py                # Landing page view
├── templates/                  # Presentation layer
│   ├── base.html               # Master layout with HTML5 landmarks & Bootstrap 5.3
│   ├── includes/               # Reusable partials
│   │   ├── navbar.html         # Main navigation bar
│   │   ├── footer.html         # Standardized institutional footer
│   │   └── messages.html       # Django messages framework alert banners
│   └── pages/
│       └── home.html           # Informational landing page
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css           # CSS custom properties (design tokens) and layout styling
│   ├── js/
│   │   └── main.js             # Lightweight vanilla JavaScript interactions
│   └── images/                 # Static graphical assets
├── media/                      # Upload directory for future student photographs and proofs
└── docs/                       # Technical documentation
    └── architecture.md         # Detailed architectural specification document
```

---

## 4. Local Environment Setup & Execution

### Step 1: Clone or Navigate to the Project Root
```bash
cd C:\Users\avoad\Downloads\studentmanagement
```

### Step 2: Set Up and Activate the Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`)*

**On Linux / macOS (Bash / Zsh):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Pinned Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env` if not already present:
```bash
# Windows PowerShell:
Copy-Item .env.example .env

# Linux / macOS:
cp .env.example .env
```
Default `.env` configuration for local development:
```dotenv
DJANGO_SECRET_KEY=edutrack-dev-key-9f8e4b3a2c1d0f5e7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_TIME_ZONE=Asia/Kolkata
DJANGO_LANGUAGE_CODE=en-in
DB_ENGINE=sqlite
```

### Step 5: Apply Database Migrations
```bash
python manage.py migrate
```

### Step 6: Create the Development Administrator Account
Run the included setup command:
```bash
python manage.py setup_dev_admin
```
*Creates initial administrator: `admin` | Password: `Admin@12345EduTrack`*

Alternatively, use Django's interactive command:
```bash
python manage.py createsuperuser
```

### Step 7: Run System Verification & Automated Tests
```bash
# Verify configuration integrity
python manage.py check

# Run the automated test suite
python manage.py test accounts
```

### Step 8: Start the Local Development Server
```bash
python manage.py runserver
```

Open your browser:
- **Public Landing Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Administration Console**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 5. Institutional Roles Hierarchy

EduTrack defines 8 institutional roles within `UserRole`:

| Role Key | Display Name | Application Scope |
|---|---|---|
| `SUPER_ADMIN` | Super Administrator | Full system administration and institutional setup |
| `COLLEGE_ADMIN` | College Administrator | College-wide configuration and department oversight |
| `PRINCIPAL` | Principal | Institution-wide reporting and academic reviews |
| `HOD` | Head of Department | Single department management (faculty, courses, classes) |
| `FACULTY` | Faculty | Assigned subjects, attendance sessions, and internal marks |
| `CLASS_ADVISOR` | Class Advisor | Assigned class cohort mentoring and review |
| `STUDENT` | Student | Personal academic timeline, results, and skill submissions |
| `GUARDIAN` | Parent or Guardian | Read-only access to linked ward's published records |

---

## 6. Troubleshooting Common Issues

1. **PowerShell execution policy error (`Activate.ps1 cannot be loaded`)**:  
   Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell.
2. **`ModuleNotFoundError: No module named 'dotenv'`**:  
   Ensure your virtual environment is activated (`.venv`) before running commands, or run `pip install -r requirements.txt`.
3. **Database port or connection error**:  
   Verify that `DB_ENGINE=sqlite` in `.env`. PostgreSQL connection settings are only evaluated if `DB_ENGINE=postgresql` is explicitly specified.
4. **Static files not loading**:  
   Verify that `DEBUG=True` in `.env` during local development so Django serves static files via `STATIC_URL = '/static/'`.
