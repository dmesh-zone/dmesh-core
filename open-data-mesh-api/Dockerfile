FROM python:3.11-slim

WORKDIR /app

# Install dependencies infrastructure (uv)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy SDK and API source
COPY open-data-mesh-sdk /app/open-data-mesh-sdk
COPY open-data-mesh-api /app/open-data-mesh-api

# Install SDK first
WORKDIR /app/open-data-mesh-sdk
RUN uv pip install -e . --system

# Install API
WORKDIR /app/open-data-mesh-api
RUN uv pip install -e . --system

EXPOSE 8000

ENV DB_TYPE=postgres
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_NAME=postgres
ENV WS_BASE_PATH=odm

CMD ["uvicorn", "open_data_mesh_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
