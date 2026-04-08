FROM python:3.12-slim

WORKDIR /app

# Install dependencies infrastructure (uv)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy SDK and API source
COPY packages/dmesh-sdk /app/packages/dmesh-sdk
COPY packages/dmesh-api /app/packages/dmesh-api

# Install SDK first (as standalone)
WORKDIR /app/packages/dmesh-sdk
RUN uv pip install . --system

# Install API
WORKDIR /app/packages/dmesh-api
# Change workspace reference to direct path reference for Docker build
RUN sed -i 's/{ workspace = true }/{ path = "..\/dmesh-sdk" }/g' pyproject.toml
RUN uv pip install . --system

EXPOSE 8000

ENV DB_TYPE=postgres
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_NAME=postgres
ENV WS_BASE_PATH=dmesh

CMD ["uvicorn", "dmesh.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
