# Use a multi-stage build for smaller final image
FROM python:3.10-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Build the final image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SANKALPA_ENV=production

# Create a non-root user
RUN adduser --disabled-password --gecos "" sankalpa

WORKDIR /app

# Install dependencies
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy the application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p /app/logs /app/memory/sessions && \
    chown -R sankalpa:sankalpa /app

# Switch to non-root user
USER sankalpa

# Expose the API port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "sankalpa.backend.enhanced_main:app", "--host", "0.0.0.0", "--port", "8000"]