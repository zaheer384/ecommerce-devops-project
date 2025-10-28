# Dockerfile - Recipe to build our application container

# Step 1: Use Python 3.9 as base image
# This gives us a lightweight Linux system with Python pre-installed
FROM python:3.9-slim

# Step 2: Set metadata about the image
LABEL maintainer="devops-team@company.com"
LABEL description="E-commerce Product API"

# Step 3: Set working directory inside container
# All commands will run from this location
WORKDIR /app

# Step 4: Install system dependencies
# These are needed for PostgreSQL connectivity
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy requirements file first
# Docker caches layers - if requirements don't change, 
# it won't reinstall packages (saves time!)
COPY requirements.txt .

# Step 6: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Copy application code
# This comes after pip install so code changes don't rebuild dependencies
COPY app.py .

# Step 8: Create non-root user for security
# Running as root in containers is a security risk
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Step 9: Expose port 5000
# This tells Docker our app listens on port 5000
EXPOSE 5000

# Step 10: Health check
# Docker will ping this endpoint to verify app is running
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Step 11: Run the application
# This command starts when container launches
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]