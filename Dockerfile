# Pull official base Python Docker image
FROM python:3.12.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for uwsgi
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project
COPY . .

# Giving Permissions
RUN chmod +x /app/wait-for-it.sh

# Change to medicare directory for Django commands
WORKDIR /app/medicare

# Collect static files
RUN python manage.py collectstatic --no-input || true

# Go back to /app
WORKDIR /app

# Expose port
EXPOSE 8000

# Run uwsgi
CMD ["uwsgi", "--ini", "/app/config/uwsgi/uwsgi.ini"]
