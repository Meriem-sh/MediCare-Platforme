import os
from .base import *
import dj_database_url

DEBUG = False

ADMINS = [
    ('meriem', 'meriemuncoding@gmail.com'),
]

ALLOWED_HOSTS = [
    "medicareproject.com",
    "www.medicareproject.com",
    "localhost",
    "127.0.0.1",
    "medicare-platform-bjlp.onrender.com",
]

# PostgreSQL Database - استخدام DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Redis
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')
CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    'https://medicare-platform-bjlp.onrender.com',
    'https://medicareproject.com',
    'https://www.medicareproject.com',
]

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
