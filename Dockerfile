# Summary: Dockerfile for Flask Application
# Description:
# Builds the ShvikiFitness Flask container using Python 3.11-slim.
# Installs all system dependencies, Python requirements, and launches the app
# using Gunicorn for production-grade performance.

FROM python:3.11-slim

# Prevent Python from writing .pyc files and force stdout logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# -------------------------------------------------
# Install system dependencies for MySQL + Python
# -------------------------------------------------
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# -------------------------------------------------
# Start Flask application using Gunicorn WSGI server
# The run.py file contains: app = create_app()
# -------------------------------------------------
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
