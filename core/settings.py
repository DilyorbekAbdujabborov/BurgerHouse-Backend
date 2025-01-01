from pathlib import Path
import decimal
import json
import environ
import os

# .env faylini o'qish uchun muhitni sozlash
env = environ.Env(
    DEBUG=(bool, False)
)

# Loyihaning asosiy katalogini aniqlash
BASE_DIR = Path(__file__).resolve().parent.parent

# .env faylini o'qish
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# .env faylidan o'zgaruvchilarni olish
DEBUG = env.bool('DEBUG', default=False)  # DEBUG boole'ga konvertatsiya qilinadi
BOT_TOKEN = env("BOT_TOKEN")
WORK_GROP_ID = env("WORK_GROP_ID")
SECRET_KEY = env('SECRET_KEY')
APP_URL=env("APP_URL", default="http://127.0.0.1")

# Yalpi IP manzillari ro'yxati
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'burgerhouseback.pythonanywhere.com', "*"]

# Django ilovalarini ro'yxatga olish
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "BurgerHouse",
    'rest_framework',
    'rest_framework_simplejwt',
    "drf_yasg",
    'corsheaders',
    "import_export"
]

# Django middleware'larini ro'yxatga olish
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Django URL konfiguratsiyasi
ROOT_URLCONF = "core.urls"

# Ma'lumotlar bazasi konfiguratsiyasi (SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Til va vaqt mintaqasi sozlamalari
LANGUAGE_CODE = "en-us" # if you need uzbek lang change this varible value to uz
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

# Statik va media fayllari konfiguratsiyasi
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# settings.py

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# CORS (Cross-Origin Resource Sharing) sozlamalari
CORS_ALLOW_ALL_ORIGINS = True

# Django shablonlar sozlamalari
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # O'zingizning shablonlar papkangizni ko'rsating
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Django REST Framework sozlamalari
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Auto field konfiguratsiyasi
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SSL yo'naltirishlarini o'chirish (HTTP to HTTPS)
SECURE_SSL_REDIRECT = False  # HTTPS yo'naltirishlarini o'chirish

# Xavfsizlik sozlamalari
SECURE_PROXY_SSL_HEADER = None  # Proxy orqali SSL sozlamalari

# Django admin panelining sozlamalari
JAZZMIN_SETTINGS = {
    "site_title": "BurgerHouse Admin",
    "site_header": "BurgerHouse",
    "site_brand": "BurgerHouse",
    "welcome_sign": "BurgerHouse admin paneliga xush kelibsiz!",
    "site_logo": "images/logo.png",  # Logotip fayli
    "topmenu_links": [
        {"name": "Bosh sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"app": "BurgerHouse"},
        {"name": "Support", "url": "https://t.me/Manager_Dilyorbek", "new_window": True},
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",
        "BurgerHouse.Foydalanuvchi": "fas fa-user-circle",
        "BurgerHouse.Address": "fas fa-map-marker-alt",
        "BurgerHouse.Category": "fas fa-list",
        "BurgerHouse.Product": "fas fa-hamburger",
        "BurgerHouse.Order": "fas fa-shopping-cart",
        "BurgerHouse.OrderProduct": "fas fa-box",
    },
    "default_icon_parents": "fas fa-chevron-circle-down",
    "default_icon_children": "fas fa-circle",
    "copyright": "BurgerHouse | By <a href='https://t.me/Manager_Dilyorbek' target='_blank'>Manager Dilyorbek</a>",
    "custom_css": None,
    "custom_js": None,
}
# settings.py
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=3000),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

