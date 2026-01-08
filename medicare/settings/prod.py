from decouple import config
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
    ".onrender.com",   
]
DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends.postgresql',
 'NAME': config('POSTGRES_DB'),
 'USER': config('POSTGRES_USER'),
 'PASSWORD': config('POSTGRES_PASSWORD'),
 'HOST': config('POSTGRES_HOST'),
 'PORT': 5432,
 }
}
REDIS_URL = 'redis://cache:6379'
CACHES['default']['LOCATION'] = REDIS_URL
CHANNEL_LAYERS['default']['CONFIG']['hosts'] = [REDIS_URL]

# Security
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

# Static files
STATIC_ROOT = '/app/staticfiles'