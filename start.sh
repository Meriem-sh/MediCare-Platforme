echo "🚀 Starting Medicare application..."
cd /app/medicare

if [ -n "$DATABASE_URL" ]; then
    # Extract hostname and port from DATABASE_URL
    DB_HOST=$(echo $DATABASE_URL | sed -E 's|.*@([^:/]+).*|\1|')
    DB_PORT=$(echo $DATABASE_URL | sed -E 's|.*:([0-9]+)/.*|\1|')
    
    echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
    /app/wait-for-it.sh $DB_HOST:$DB_PORT --timeout=60 --strict -- echo "✅ PostgreSQL is ready!"
else
    echo "⚠️ DATABASE_URL not set, skipping wait-for-it"
fi

echo "📊 Running migrations..."
python manage.py migrate --no-input

echo "👤 Creating admin users..."
python manage.py ensure_admin

if [ "$LOAD_FAKE_DATA" = "true" ]; then
    echo "🎲 Generating fake data with populate_data..."
    python manage.py populate_data
fi

echo "✅ Setup complete! Starting uWSGI..."
cd /app
exec uwsgi --http 0.0.0.0:8000 --chdir /app/medicare --module medicare.wsgi:application --master --processes 4 --threads 2 --vacuum --die-on-term
