FROM python:3.12.3

# Install system dependencies including dos2unix
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Fix line endings for shell scripts
RUN dos2unix /app/wait-for-it.sh /app/start.sh

# Make shell scripts executable
RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/start.sh

# Start command
CMD ["/app/start.sh"]
