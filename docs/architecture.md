# EduTrack — Architecture Documentation

## 1. Architectural Style: Modular Monolith

EduTrack is designed as a modular Django monolithic web application. For real-college deployment, a well-structured monolith provides significant advantages over microservices or split decoupled frontends:
- **ACID Transactions**: Vital when recording student marks and exam results across related tables.
- **Single Source of Truth**: Django's integrated ORM, authentication, and permission system avoids distributed auth complexities.
- **Maintainability**: Low operational overhead for college IT departments.
- **Data Integrity**: Foreign keys and database-level constraints guarantee that historical academic records remain valid.

---

## 2. Directory Layout & Responsibilities (Phase 1)

```text
edutrack/
├── manage.py                   # Django CLI management entrypoint
├── requirements.txt            # Pinned dependencies (Django 5.1, python-dotenv, Pillow, ReportLab)
├── .env                        # Local development environment configuration (git-ignored)
├── .env.example                # Template with placeholder configuration
├── .gitignore                  # Git exclusion rules for secrets, DB, and media
├── README.md                   # Setup guide, commands, and project status
├── config/                     # Django project configuration package
│   ├── __init__.py
│   ├── settings.py             # Settings reading .env, configuring auth, DB, static/media
│   ├── urls.py                 # Root URL router (/admin/ and /)
│   ├── asgi.py                 # ASGI entrypoint for asynchronous workers
│   └── wsgi.py                 # WSGI entrypoint for standard web servers
├── accounts/                   # User authentication & institutional role management
│   ├── __init__.py
│   ├── admin.py                # UserAdmin integration for role assignment
│   ├── apps.py                 # App configuration
│   ├── models.py               # Custom User model extending AbstractUser & UserRole enum
│   ├── managers.py             # UserManager with unique email enforcement
│   ├── tests.py                # Automated unit tests for Phase 1
│   ├── migrations/             # Database migrations
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
    └── architecture.md         # This architectural specification document
```

---

## 3. Custom User Model Foundation

Configured via `AUTH_USER_MODEL = "accounts.User"` prior to the initial database migration.

### Institutional Roles (`UserRole` TextChoices)
The system defines 8 institutional roles:
1. `SUPER_ADMIN` &mdash; Super Administrator
2. `COLLEGE_ADMIN` &mdash; College Administrator
3. `PRINCIPAL` &mdash; Principal
4. `HOD` &mdash; Head of Department
5. `FACULTY` &mdash; Faculty
6. `CLASS_ADVISOR` &mdash; Class Advisor
7. `STUDENT` &mdash; Student (default for standard accounts)
8. `GUARDIAN` &mdash; Parent or Guardian

### Key Architectural Distinctions:
- **Application Role vs Django Permissions**: An application role (`role`) is distinct from Django's `is_staff` or `is_superuser` flags. Superuser privileges must never be granted automatically merely by assigning the `SUPER_ADMIN` role.
- **Department Association**: Department foreign keys are intentionally omitted in Phase 1. They will be connected in Phase 4 when the `departments` module is created.
- **No Self-Assignment**: Roles cannot be selected during any public form. Only authorized administrators manage user roles.

---

## 4. Environment & Database Strategy

### Environment Configuration
- Configuration is loaded via `python-dotenv` from `BASE_DIR / '.env'` (derived from the settings file, not the working directory).
- Variables supported:
  - `DJANGO_SECRET_KEY`: Cryptographic signing key.
  - `DJANGO_DEBUG`: Safely parsed boolean (`True` in dev, strictly `False` in production).
  - `DJANGO_ALLOWED_HOSTS`: Comma-separated allowed hostnames.
  - `DJANGO_TIME_ZONE`: Defaults to `Asia/Kolkata`.
  - `DJANGO_LANGUAGE_CODE`: Defaults to `en-in`.
  - `DB_ENGINE`: `sqlite` for development; `postgresql` for production.

### SQLite vs PostgreSQL
- **Development**: Local development utilizes SQLite (`db.sqlite3`), requiring zero configuration for beginners.
- **Production**: PostgreSQL will be used for production. Switching involves setting `DB_ENGINE=postgresql` and database connection credentials in `.env`.
- *Note on Migration*: Migrating existing production data from SQLite to PostgreSQL is never automatic or trivial; it requires data dump reconciliation, index verification, and schema validation.

---

## 5. Planned Future Module Boundaries

Future phases will introduce modular applications following single-responsibility principles:
- **`departments` (Phase 4)**: Departments, courses, academic batches, and faculty assignments.
- **`students` (Phase 4)**: Permanent student identities, profiles, and guardian relationships.
- **`academics` (Phase 5 & 6)**: Semesters, subjects, assessments, and examination marks.
- **`attendance` (Phase 6)**: Subject-wise attendance sessions, records, and threshold tracking.
- **`progress` (Phase 7)**: Multi-year academic progress comparison and analytics.
- **`achievements` (Phase 8)**: Student skill portfolios, certificates, and verification workflows.
- **`reports` (Phase 10)**: Server-side ReportLab PDF transcript and report generation.
- **`notifications` (Phase 10)**: Internal alerts and notice board.
- **`insights` (Phase 11)**: Deterministic performance drop detection and optional Gemini AI integration.
- **`audit` (Phase 12)**: Immutable audit logging of sensitive marks, attendance, and role changes.

---

## 6. Mandatory Security Rules for Future Phases

All subsequent phases must uphold the following architectural constraints:
1. **Server-Side Authorization**: Every view, downloadable report, and endpoint must enforce permissions on the server. Never rely on hiding UI elements in templates.
2. **Department Queryset Scoping**: HODs and faculty must only query records belonging to their assigned department or course.
3. **Student & Guardian Data Isolation**: Students and guardians may only access their own records. Guardians access only verified linked wards.
4. **Historical Immutability**: Advancing to a new academic year must create a new enrollment record rather than overwriting past marks.
5. **No Secrets in Source Control**: Production secrets, API keys, and database passwords must never be committed to Git.
