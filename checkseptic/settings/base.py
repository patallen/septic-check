import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = []

INSTALLED_APPS = ["django.contrib.contenttypes", "api"]
MIDDLEWARE = []

ROOT_URLCONF = "checkseptic.urls"
WSGI_APPLICATION = "checkseptic.wsgi.application"

<<<<<<< HEAD
HOUSE_CANARY_API_KEY = os.environ.get("HOUSE_CANARY_API_KEY")
HOUSE_CANARY_API_SECRET = os.environ.get("HOUSE_CANARY_API_SECRET")
HOUSE_CANARY_BASE_URL = os.environ.get(
    "HOUSE_CANARY_BASE_URL", "https://api.housecanary.com/v2"
)
=======
HOUSE_CANARY_API_KEY = os.environ.get("HOUSE_CANARY_API_KEY", "")
HOUSE_CANARY_API_SECRET = os.environ.get("HOUSE_CANARY_API_SECRET", "")
HOUSE_CANARY_BASE_URL = os.environ.get("HOUSE_CANARY_BASE_URL", "")
>>>>>>> Refactor view and supporting code to be async
