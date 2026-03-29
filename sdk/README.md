# Open Data Mesh Python SDK

A high-level Python SDK for managing Open Data Mesh resources (Data Products and Data Contracts). This SDK encapsulates all business logic, validation, and enrichment required to interact with an Open Data Mesh environment.

## Architecture Layers

This project is structured into the following decoupled layers:

1. **Python SDK (Core Logic)**: The foundation of the system. Contains models, validation, enrichment, and the `DataMeshService` which orchestrates all operations.
2. **Persistency**: Flexible data storage layer. Supports multiple repositories:
   - `SQLiteRepository`: Recommended for local development and testing. No external dependencies required.
   - `PostgresRepository`: Recommended for production environments. Used with external PostgreSQL databases.
   - `InMemoryRepository`: Ideal for unit testing and ephemeral environments.
3. **CLI**: A command-line interface built on top of the Python SDK for manual interaction and automation.
4. **REST API**: A FastAPI-powered web layer that exposes the SDK functionality via standard HTTP endpoints.

## Installation

```bash
pip install open_data_mesh_sdk
```

## Quick Start (Local Development)

The SDK makes it easy to get started locally using SQLite:

```python
from open_data_mesh_sdk import DataMeshService, SQLiteRepository

# Initialize with a local SQLite database
repository = SQLiteRepository("odm.db")
service = DataMeshService(repository)

# Create a Data Product
dp_spec = {
    "apiVersion": "v1.0.0",
    "kind": "DataProduct",
    "domain": "sales",
    "name": "annual-revenue",
    "version": "1.0.0"
}

dp = service.create_data_product(dp_spec)
print(f"Created Data Product: {dp.id}")
```

## Production Deployment (PostgreSQL)

In production, the SDK should be configured to use a PostgreSQL database:

```python
from open_data_mesh_sdk import DataMeshService, PostgresRepository
from psycopg2 import pool

# Initialize a connection pool
connection_pool = pool.SimpleConnectionPool(1, 10, host="your-db-host", ...)

# Initialize with the Postgres repository
repository = PostgresRepository(connection_pool)
service = DataMeshService(repository)
```

## Documentation

- **Models**: [open_data_mesh_sdk.core.models](src/open_data_mesh_sdk/core/models.py)
- **Service API**: [open_data_mesh_sdk.core.service](src/open_data_mesh_sdk/core/service.py)
- **Examples**: [examples/](examples/)

## Local CLI

If you have the `open-data-mesh-cli` installed, you can use the `odm` command to interact with the local data mesh environment:

```bash
odm init
odm put dp sales_report.yaml
odm list dps
```
