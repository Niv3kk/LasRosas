"""
Django settings for core project.
"""

from pathlib import Path
import os
import environ

# =========================
# BASE / ENV
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, True),
)
# Carga variables desde backend/.env (si existe)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# =========================
# SECURITY / DEBUG
# =========================
SECRET_KEY = env('SECRET_KEY', default='django-insecure-dev-key-no-usar-en-prod')
DEBUG = env.bool('DEBUG', default=True)

# Coma-separado en .env (ej: "127.0.0.1,localhost")
ALLOWED_HOSTS = [h.strip() for h in env('ALLOWED_HOSTS', default='').split(',') if h.strip()]

# =========================
# APPS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # si ya instalaste DRF
    'api.apps.ApiConfig',             # <--- asegúrate de tener esta línea
    "corsheaders",
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # CORS debe ir antes de CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =========================
# URLS / WSGI
# =========================
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# =========================
# DATABASE
# =========================
# Usa DATABASE_URL del .env (formato Supabase) y obliga SSL
DATABASES = {
    'default': env.db('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}
if DATABASES['default']['ENGINE'].endswith('postgresql'):
    # si tu cadena no trae sslmode, lo forzamos aquí
    DATABASES['default'].setdefault('OPTIONS', {})
    DATABASES['default']['OPTIONS'].setdefault('sslmode', 'require')

# =========================
# PASSWORD VALIDATORS
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# I18N / TZ
# =========================
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = True

# =========================
# STATIC
# =========================
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# CORS (para Vite en dev)
# =========================
# Define en .env (coma-separado): "http://127.0.0.1:5173,http://localhost:5173"
CORS_ALLOWED_ORIGINS = [o.strip() for o in env('CORS_ALLOWED_ORIGINS', default='').split(',') if o.strip()]
