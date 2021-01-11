import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "vt%3x^46o=+x4gm-3p$5d$&2qh#kv8i8y+f$#=-g4h2!t3_6hw"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = ["django.contrib.contenttypes", "api"]

MIDDLEWARE = []

ROOT_URLCONF = "checkseptic.urls"

WSGI_APPLICATION = "checkseptic.wsgi.application"

HOUSE_CANARY_API_KEY = os.environ.get("HOUSE_CANARY_API_KEY")
HOUSE_CANARY_API_SECRET = os.environ.get("HOUSE_CANARY_API_SECRET")
HOUSE_CANARY_BASE_URL = os.environ.get("HOUSE_CANARY_BASE_URL")
