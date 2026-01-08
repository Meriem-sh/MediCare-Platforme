FROM python:3.12.3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=medicare.settings.prod

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Make scripts executable
RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/start.sh

# Collect static files
WORKDIR /app/medicare
RUN python manage.py collectstatic --no-input

WORKDIR /app

EXPOSE 8000

# Use start.sh
CMD ["/app/start.sh"]
