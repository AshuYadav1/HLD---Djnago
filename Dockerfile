# Stage 1: Builder
FROM python:3.8-slim-buster AS builder

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY task2/requirements.txt .

# Disable C extensions for backports.zoneinfo
ENV ZONEINFO_NO_C=1

# Install Python dependencies
RUN pip install --user --require-hashes -r requirements.txt

# Stage 2: Runtime

FROM python:3.8-slim-buster
WORKDIR /app

# Copy from builder and project files
COPY --from=builder /root/.local /root/.local
COPY .. .
CMD ["python", "manage.py", "process_campaigns"]