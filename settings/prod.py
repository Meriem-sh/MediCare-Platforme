import os
from .base import *

DEBUG = False

ADMINS = [
    ('meriem', 'admin@example.com'),
    ('Meriem-Sh', 'meriemuncoding@gmail.com'),
]

ALLOWED_HOSTS = [
    "medicareproject.com",
    "www.medicareproject.com",
    "localhost",
    "127.0.0.1",
    "*.onrender.com",
    'medicare-platform-bjlp.onrender.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Redis Upstash
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')
CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]

# Security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
