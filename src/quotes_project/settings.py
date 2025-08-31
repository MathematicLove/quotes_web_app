import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    print("WARNING: DJANGO_SECRET_KEY not set, using fallback key")
    SECRET_KEY = 'dev-secret-key-for-development-only-change-in-production'
else:
    print(f"SECRET_KEY loaded from environment: {SECRET_KEY[:10]}...")

DEBUG = os.getenv('DJANGO_DEBUG', '1').lower() in ('1', 'true', 'yes')
print(f"DEBUG setting: {DEBUG}")

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
print(f"ALLOWED_HOSTS: {ALLOWED_HOSTS}")

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes',
    'django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'quotes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'quotes_project.urls'
TEMPLATES = [{
    'BACKEND':'django.template.backends.django.DjangoTemplates',
    'DIRS':[], 'APP_DIRS':True,
    'OPTIONS':{'context_processors':[
        'django.template.context_processors.debug','django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages'
    ]}
}]
WSGI_APPLICATION = 'quotes_project.wsgi.application'

import dj_database_url

DATABASE_URL = os.getenv('DATABASE_URL')
print(f"DATABASE_URL: {DATABASE_URL[:50] if DATABASE_URL else 'Not set'}...")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
    print("Using DATABASE_URL from environment")
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'quotes'),
            'USER': os.getenv('POSTGRES_USER', 'quotes'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'quotes'),
            'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
            'PORT': '5432',
        }
    }
    print("Using local database configuration")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'quotes/static'),
]

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True