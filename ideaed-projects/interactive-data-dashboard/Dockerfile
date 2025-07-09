# Multi-stage Dockerfile for Interactive Data Dashboard
# Optimized for production deployment with minimal image size

# Build stage
FROM python:3.11-slim as builder

# Set build arguments
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

# Set environment variables for build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install build && \
    pip install .

# Production stage
FROM python:3.11-slim as production

# Set metadata labels
LABEL maintainer="Interactive Data Dashboard Team <contact@example.com>" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="interactive-data-dashboard" \
      org.label-schema.description="Interactive data visualization dashboard built with Streamlit, Pandas, and Plotly" \
      org.label-schema.url="https://github.com/your-org/interactive-data-dashboard" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/your-org/interactive-data-dashboard" \
      org.label-schema.vendor="Interactive Data Dashboard Team" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true \
    STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200 \
    STREAMLIT_THEME_BASE=light \
    STREAMLIT_THEME_PRIMARY_COLOR=#FF6B6B \
    STREAMLIT_THEME_BACKGROUND_COLOR=#FFFFFF \
    STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR=#F0F2F6 \
    STREAMLIT_THEME_TEXT_COLOR=#262730

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user for security
RUN groupadd -r streamlit && useradd -r -g streamlit streamlit

# Create application directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source code
COPY src/ ./src/
COPY .env.example ./.env

# Create necessary directories
RUN mkdir -p /app/data /app/logs /app/uploads /app/exports && \
    chown -R streamlit:streamlit /app

# Switch to non-root user
USER streamlit

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Set the default command
CMD ["streamlit", "run", "src/interactive_data_dashboard/main.py", \
     "--server.headless", "true", \
     "--server.port", "8501", \
     "--server.address", "0.0.0.0", \
     "--browser.gatherUsageStats", "false"]

# Development stage (optional)
FROM production as development

# Switch back to root for development dependencies
USER root

# Install development dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    vim \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Install development Python packages
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    black \
    ruff \
    mypy \
    jupyter \
    ipython

# Copy development files
COPY tests/ ./tests/
COPY pytest.ini ./
COPY Makefile ./

# Set development environment variables
ENV STREAMLIT_SERVER_RUN_ON_SAVE=true \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=poll

# Switch back to streamlit user
USER streamlit

# Development command with auto-reload
CMD ["streamlit", "run", "src/interactive_data_dashboard/main.py", \
     "--server.headless", "true", \
     "--server.port", "8501", \
     "--server.address", "0.0.0.0", \
     "--server.runOnSave", "true", \
     "--server.fileWatcherType", "poll"]