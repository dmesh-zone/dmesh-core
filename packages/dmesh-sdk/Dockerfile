FROM python:3.12-slim

WORKDIR /app

# Install dependencies infrastructure (uv)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy all packages (to allow workspace-like builds)
COPY packages /app/packages

# Install SDK
WORKDIR /app/packages/dmesh-sdk
RUN uv pip install . --system

# Attempt to install API if it exists (for compatibility with dmesh-api service)
RUN if [ -d "/app/packages/dmesh-api" ]; then \
        cd /app/packages/dmesh-api && \
        sed -i 's/{ workspace = true }/{ path = "..\/dmesh-sdk" }/g' pyproject.toml && \
        uv pip install . --system; \
    fi

WORKDIR /app
CMD ["python"]
