#!/bin/bash
set -e

echo "🚀 Starting Medicare application..."

# Print environment info
echo "📍 Working directory: $(pwd)"
echo "📍 Python version: $(python --version)"
echo "📍 Django settings: $DJANGO_SETTINGS_MODULE"

# الانتقال إلى مجلد المشروع
cd /app/medicare

# جمع الملفات الثابتة
echo "📊 Collecting static files..."
python manage.py collectstatic --noinput

# Retry logic لـ migrations
echo "📊 Running migrations with retry..."
MAX_RETRIES=10
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if python manage.py migrate --noinput; then
        echo "✅ Migrations completed successfully!"
        break
    else
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "⚠️ Migration attempt $RETRY_COUNT failed, retrying in 5 seconds..."
            sleep 5
        else
            echo "❌ Migrations failed after $MAX_RETRIES attempts"
            echo "📋 Database connection info:"
            python -c "import os; print(f'DATABASE_URL: {os.environ.get(\"DATABASE_URL\", \"NOT SET\")[:50]}...')"
            exit 1
        fi
    fi
done

# إنشاء admin user 1
if [ -n "$ADMIN1_USERNAME" ] && [ -n "$ADMIN1_PASSWORD" ] && [ -n "$ADMIN1_EMAIL" ]; then
    echo "👤 Creating admin user 1..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = '$ADMIN1_USERNAME'
email = '$ADMIN1_EMAIL'
password = '$ADMIN1_PASSWORD'

if User.objects.filter(username=username).exists():
    print(f'ℹ️  User {username} already exists')
else:
    User.objects.create_superuser(username, email, password)
    print(f'✅ Superuser {username} created successfully')
EOF
else
    echo "⚠️ Admin 1 credentials not provided"
fi

# إنشاء admin user 2
if [ -n "$ADMIN2_USERNAME" ] && [ -n "$ADMIN2_PASSWORD" ] && [ -n "$ADMIN2_EMAIL" ]; then
    echo "👤 Creating admin user 2..."
    python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
username = '$ADMIN2_USERNAME'
email = '$ADMIN2_EMAIL'
password = '$ADMIN2_PASSWORD'

if User.objects.filter(username=username).exists():
    print(f'ℹ️  User {username} already exists')
else:
    User.objects.create_superuser(username, email, password)
    print(f'✅ Superuser {username} created successfully')
EOF
else
    echo "⚠️ Admin 2 credentials not provided"
fi

# تخطي fake data في production
if [ "$LOAD_FAKE_DATA" = "true" ]; then
    echo "🎲 Generating fake data..."
    python manage.py populate_data || echo "⚠️ Data population skipped"
else
    echo "⏭️ Skipping fake data generation (LOAD_FAKE_DATA != true)"
fi

echo "✅ Setup complete! Starting Gunicorn..."

# تشغيل Gunicorn
exec gunicorn medicare.wsgi:application \
      --bind 0.0.0.0:${PORT:-8000} \
      --workers ${WEB_CONCURRENCY:-2} \
      --threads 4 \
      --timeout 120 \
      --access-logfile - \
      --error-logfile - \
      --log-level info
