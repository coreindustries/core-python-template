# =============================================================================
# Python Application Dockerfile
# Multi-stage build for development and production
# =============================================================================

# -----------------------------------------------------------------------------
# Base stage: Common setup
# -----------------------------------------------------------------------------
FROM python:3.12-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# -----------------------------------------------------------------------------
# Dependencies stage: Install Python dependencies
# -----------------------------------------------------------------------------
FROM base AS dependencies

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install dependencies (without dev dependencies for smaller image)
RUN uv sync --frozen --no-install-project

# -----------------------------------------------------------------------------
# Development stage: Full development environment
# -----------------------------------------------------------------------------
FROM base AS development

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# Install all dependencies including dev
RUN uv sync --frozen --no-install-project

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/
COPY prisma/ ./prisma/

# Generate Prisma client
RUN uv run prisma generate

# Install the project
RUN uv sync --frozen

# Expose port
EXPOSE 8000

# Run with hot reload
CMD ["uv", "run", "uvicorn", "project_name.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# -----------------------------------------------------------------------------
# Production stage: Minimal production image
# -----------------------------------------------------------------------------
FROM base AS production

# Create non-root user for security
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

# Copy installed dependencies from dependencies stage
COPY --from=dependencies /app/.venv /app/.venv

# Copy source code and dependency files
COPY src/ ./src/
COPY prisma/ ./prisma/
COPY pyproject.toml uv.lock ./

# Install the project
RUN uv sync --frozen

# Generate Prisma client
RUN uv run prisma generate

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uv", "run", "uvicorn", "project_name.main:app", "--host", "0.0.0.0", "--port", "8000"]
