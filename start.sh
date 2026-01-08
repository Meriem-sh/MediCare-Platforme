#!/bin/bash

echo "🚀 Starting Medicare application..."
cd /app/medicare

echo "📊 Running migrations..."
python manage.py migrate --no-input

echo "👤 Creating admin users..."
python manage.py ensure_admin

# تشغيل البيانات التجريبية (إذا مفعّل)
if [ "$LOAD_FAKE_DATA" = "true" ]; then
    echo "🎲 Generating fake data with populate_data..."
    python manage.py populate_data
fi

echo "✅ Setup complete! Starting uWSGI..."
cd /app
exec uwsgi --http 0.0.0.0:8000 --chdir /app/medicare --module medicare.wsgi:application --master --processes 4 --threads 2 --vacuum --die-on-term
