# Bengali Telegram Bot - Docker Configuration
# বাংলা টেলিগ্রাম বট - ডকার কনফিগারেশন

FROM python:3.11-slim

LABEL maintainer="Sagar Mandal <sagar@example.com>"
LABEL description="Modern Bengali Telegram Bot"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs uploads static/temp

# Create non-root user
RUN groupadd -r botuser && useradd -r -g botuser botuser
RUN chown -R botuser:botuser /app
USER botuser

# Expose port (if needed for webhooks)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from config.settings import config; print('Bot healthy')" || exit 1

# Default command
CMD ["python", "main.py"]