import os
from .base import *
import dj_database_url

DEBUG = False

ADMINS = [
    ('meriem', 'meriemuncoding@gmail.com'),
]

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'medicare-platform-bjlp.onrender.com').split(',')

# PostgreSQL Database - استخدام DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL environment variable is not set!")

print(f"🔍 DATABASE_URL configured: {DATABASE_URL[:50]}...")

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Redis Configuration (Upstash)
REDIS_URL = os.environ.get('REDIS_URL')

if REDIS_URL:
    print(f"🔍 Redis URL configured: {REDIS_URL[:30]}...")
    
    # Override Cache with Upstash Redis
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 20,
                    'retry_on_timeout': True,
                },
            }
        }
    }
    
    # Override Channel Layers with Upstash Redis
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [REDIS_URL],
            },
        },
    }
else:
    print("⚠️ Redis URL not configured, using dummy cache")
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# Security Settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    'https://medicare-platform-bjlp.onrender.com',
    'https://medicareproject.com',
    'https://www.medicareproject.com',
]

# HTTPS Settings - تعطيل SSL_REDIRECT لتجنب redirect loop في Render
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging للتشخيص
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
# Email Configuration (Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'MediCare <noreply@medicare.com>'
SERVER_EMAIL = EMAIL_HOST_USER

# If email is not configured, use console backend for testing
if not EMAIL_HOST_USER:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    print("⚠️ Email not configured, using console backend")
