import os
import sys
from pathlib import Path

import dotenv
from split_settings.tools import include

dotenv.load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str(os.getenv("SECRET_KEY"))

DEBUG = str(os.getenv("DEBUG", "False")) == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "movies.apps.MoviesConfig",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]


ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/data/static/"

# Медиа-файлы (загруженные пользователями)
MEDIA_URL = "/media/"
MEDIA_ROOT = "/data/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOCALE_PATHS = ["movies/locale"]

CORS_ALLOWED_ORIGINS = ["http://localhost:80"]

include(
    "components/database.py",
    "components/templates.py",
    "components/internationalization.py",
    "components/password_validator.py",
)
