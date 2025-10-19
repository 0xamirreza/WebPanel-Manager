FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser

# Create data directory and set permissions
RUN mkdir -p /app/data && \
    chown -R appuser:appuser /app

USER appuser

# Expose port
EXPOSE 44553

# Run the application
CMD ["python", "run.py"]
