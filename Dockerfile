# Stage 1: Builder
FROM python:3.8-slim-buster AS builder

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first
COPY task2/requirements.txt .

# Disable C extensions for backports.zoneinfo
ENV ZONEINFO_NO_C=1

# Install Python dependencies
RUN pip install --user --require-hashes -r requirements.txt

# Stage 2: Runtime
FROM python:3.8-slim-buster

WORKDIR /app

# Copy from builder
COPY --from=builder /root/.local /root/.local

# Copy project files
COPY . .

# Ensure the settings module is correct
ENV DJANGO_SETTINGS_MODULE=task.settings.production

# Update PATH
ENV PATH=/root/.local/bin:$PATH

# Command to run
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]