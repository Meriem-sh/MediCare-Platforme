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

# Expose port
EXPOSE 8000
