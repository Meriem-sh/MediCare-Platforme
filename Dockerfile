# Pull official base Python Docker image
FROM python:3.12.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project
COPY . .

# Giving Permissions
RUN chmod +x /app/wait-for-it.sh

# Collect static files
RUN cd medicare && DJANGO_SETTINGS_MODULE=medicare.settings.prod python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD cd medicare && python manage.py migrate && uwsgi --ini /app/config/uwsgi/uwsgi.ini
