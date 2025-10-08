"""
Django settings for config project.

This settings module is environment-driven and configures REST API, token auth,
CORS, and service integrations to GitLab and SonarQube.
"""
from pathlib import Path
import os
import environ

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Env setup
env = environ.Env(
    DJANGO_DEBUG=(bool, True),
)
environ.Env.read_env(os.path.join(BASE_DIR, ".env")) if os.path.exists(os.path.join(BASE_DIR, ".env")) else None

# Core settings
SECRET_KEY = env("DJANGO_SECRET_KEY", default="insecure-dev-key")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*", ".kavia.ai", "localhost", "127.0.0.1", "testserver"])

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "corsheaders",
    # Local apps
    "api",
    "projects",
    "scans",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database (SQLite for MVP)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS and proxy handling
CORS_ALLOW_ALL_ORIGINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
X_FRAME_OPTIONS = "ALLOWALL"

# DRF configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# Service integration settings read from env
GITLAB_BASE_URL = env("GITLAB_BASE_URL", default="https://gitlab.com")
GITLAB_TOKEN = env("GITLAB_TOKEN", default="")
SONARQUBE_BASE_URL = env("SONARQUBE_BASE_URL", default="http://localhost:9000")
SONARQUBE_TOKEN = env("SONARQUBE_TOKEN", default="")

# Logging
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": True},
        "projects": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "scans": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "services": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
    },
}
