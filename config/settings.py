"""
Django settings for EduTrack project.

Phase 1: Project Setup, Architecture, Configuration, and UI Foundation.
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# Build paths inside the project: BASE_DIR is the workspace root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env located at BASE_DIR (not CWD)
load_dotenv(BASE_DIR / '.env')


def get_bool_env(name: str, default: bool = False) -> bool:
    """Safely parse boolean environment variables without treating 'False' as True."""
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ('true', '1', 't', 'yes', 'y')


# Security Settings
# Support both DJANGO_SECRET_KEY and legacy SECRET_KEY
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY') or os.getenv('SECRET_KEY')
if not SECRET_KEY:
    if get_bool_env('DJANGO_DEBUG', True):
        # Development fallback with clear log notice
        SECRET_KEY = 'insecure-dev-fallback-key-for-local-development-only'
    else:
        raise ValueError("DJANGO_SECRET_KEY must be set when running in production (DEBUG=False).")

DEBUG = get_bool_env('DJANGO_DEBUG', get_bool_env('DEBUG', True))

raw_allowed_hosts = os.getenv('DJANGO_ALLOWED_HOSTS') or os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost')
ALLOWED_HOSTS = [h.strip() for h in raw_allowed_hosts.split(',') if h.strip()]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom Core Applications
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'


# Database Configuration
# Defaults to SQLite for local development; structured for future PostgreSQL deployment.

DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite').lower()

if DB_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'edutrack'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / os.getenv('DB_NAME', 'db.sqlite3'),
        }
    }


# Custom User Model (Configured before initial migrations)
AUTH_USER_MODEL = 'accounts.User'


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization & Time Zone
LANGUAGE_CODE = os.getenv('DJANGO_LANGUAGE_CODE', 'en-in')
TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'Asia/Kolkata')
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files (Future student uploads and certificates)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
