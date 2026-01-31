# Multi-stage build for optimized production and development Docker images
# Stage 1: Builder - compile and resolve dependencies
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install system build dependencies early
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements*.txt ./

# Upgrade pip, setuptools, wheel for better binary wheel support
RUN pip install --upgrade --no-cache-dir pip setuptools wheel

# Install Python dependencies with proper wheel caching
# Use minimal requirements for faster builds (RAG optional)
RUN pip install --no-cache-dir \
    --target /install \
    -r requirements-minimal.txt


# Stage 2: Runtime - minimal image with runtime dependencies only
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only runtime system dependencies (postgresql-client for health checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local/lib/python3.11/site-packages/

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
RUN chmod +x /app/entrypoint.sh
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
ENTRYPOINT ["/app/entrypoint.sh"]
