# Open Data Mesh REST API (FastAPI)

Building on the `open-data-mesh-sdk`, this REST API provides a flexible interface for managing Data Products and Data Contracts via HTTP.

## Key Features

- **FastAPI-powered**: Fully documented OpenAPI 3.0 compliant endpoints.
- **Layered Architecture**: Decoupled from core business logic (SDK) and data storage (Persistency).
- **Environment Driven**: Supports multiple database engines (SQLite, Postgres) based on configuration.
- **Deployable Anywhere**: Standalone, Dockerized, or AWS Lambda (using Mangum).

## Getting Started (Standalone)

Run the API locally with uvicorn:

```bash
uv run uvicorn open_data_mesh_api.main:app --reload
```

By default, this will initialize with a local `odm.db` SQLite database.

## Environment Variables

| Variable | Description | Default |
| -------- | ----------- | ------- |
| `DB_TYPE` | Either `sqlite` or `postgres` | `sqlite` |
| `DB_PATH` | Path to the SQLite database (if `DB_TYPE=sqlite`) | `odm.db` |
| `DB_HOST` | Postgres host (if `DB_TYPE=postgres`) | `localhost` |
| `DB_PORT` | Postgres port (if `DB_TYPE=postgres`) | `5432` |
| `DB_USER` | Postgres user (if `DB_TYPE=postgres`) | `postgres` |
| `DB_PASSWORD`| Postgres password (if `DB_TYPE=postgres`) | `postgres` |
| `DB_NAME` | Postgres database name (if `DB_TYPE=postgres`) | `postgres` |
| `WS_BASE_PATH`| Base path for all API endpoints | `odm` |

## Deployment

### Docker

Build and run with a production-grade container:

```bash
docker build -t open-data-mesh-api .
docker run -p 8000:8000 open-data-mesh-api
```

### AWS Lambda

This project includes `Mangum` wrapping, making it ready for deployment as an AWS Lambda function behind an API Gateway.

## API Endpoints

-   `POST /odm/dps`: Create Data Product
-   `GET /odm/dps/{id}`: Get Data Product
-   `GET /odm/dps`: List Data Products
-   `PUT /odm/dps/{id}`: Update Data Product
-   `DELETE /odm/dps/{id}`: Delete Data Product
-   `POST /odm/dps/{id}/dcs`: Create Data Contract for Data Product
-   `GET /odm/dcs/{id}`: Get Data Contract
-   `GET /odm/dcs`: List Data Contracts
-   `DELETE /odm/dcs/{id}`: Delete Data Contract
