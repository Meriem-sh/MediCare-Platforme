#!/bin/bash
set -e

echo "🚀 Starting Medicare application..."

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
            exit 1
        fi
    fi
done

# إنشاء admin user
echo "👤 Creating admin users..."
python manage.py ensure_admin || echo "⚠️ Admin creation skipped"

# تخطي fake data في production
if [ "$LOAD_FAKE_DATA" = "true" ]; then
    echo "🎲 Generating fake data..."
    python manage.py populate_data || echo "⚠️ Data population skipped"
else
    echo "⏭️ Skipping fake data generation"
fi

echo "✅ Setup complete! Starting uWSGI..."

# تشغيل uWSGI (من مجلد medicare)
exec uwsgi --http 0.0.0.0:8000 \
      --module medicare.wsgi:application \
      --master \
      --processes 4 \
      --threads 2 \
      --max-requests 5000 \
      --harakiri 60 \
      --http-timeout 60 \
      --socket-timeout 60 \
      --enable-threads
