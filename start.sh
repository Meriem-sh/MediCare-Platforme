#!/bin/bash
set -e

echo "🚀 Starting Medicare application..."

# استخراج HOST و PORT من DATABASE_URL بشكل صحيح
if [ -n "$DATABASE_URL" ]; then
    # استخراج HOST (بين @ و /)
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:\/]*\).*/\1/p')
    
    # استخراج PORT (بين : و /)
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    # إذا لم يكن هناك PORT في URL، استخدم 5432
    if [ -z "$DB_PORT" ]; then
        DB_PORT=5432
    fi
    
    echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
    ./wait-for-it.sh $DB_HOST:$DB_PORT --timeout=60 --strict
else
    echo "⚠️ DATABASE_URL not set, skipping database wait"
fi

# جمع الملفات الثابتة
echo "📊 Collecting static files..."
python manage.py collectstatic --noinput

# تنفيذ migrations
echo "📊 Running migrations..."
python manage.py migrate --noinput || echo "⚠️ Migrations failed, continuing..."

# إنشاء admin user
echo "👤 Creating admin users..."
python manage.py ensure_admin || echo "⚠️ Admin creation failed, continuing..."

# إنشاء بيانات تجريبية (فقط إذا كان LOAD_FAKE_DATA=true)
if [ "$LOAD_FAKE_DATA" = "true" ]; then
    echo "🎲 Generating fake data..."
    python manage.py populate_data || echo "⚠️ Data population failed, continuing..."
else
    echo "⏭️ Skipping fake data generation (LOAD_FAKE_DATA not set to true)"
fi

echo "✅ Setup complete! Starting uWSGI..."

# تشغيل uWSGI
uwsgi --http 0.0.0.0:8000 \
      --module medicare.wsgi:application \
      --master \
      --processes 4 \
      --threads 2 \
      --max-requests 5000 \
      --harakiri 30 \
      --http-timeout 30 \
      --socket-timeout 30
