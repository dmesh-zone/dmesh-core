# dmesh-core

A modern, high-performance toolkit for managing **Open Data Mesh** specifications, focusing on Data Products and Data Contracts. This repository provides a unified `uv` workspace for the core SDK, REST API, and CLI components.

## 🏗️ Architecture Overview

The project is structured as a modular Python workspace with a clear separation of concerns:

-   **`dmesh-sdk`**: The core logic layer. Supporting CRUD operations for Open Data Product and Open Data Contract specifications
-   **`dmesh-cli`**: A Typer-powered command-line interface for local-first development. It allows users to initialize a local environment, manage specifications, and interact with PostgreSQL backend.
-   **`dmesh-api`**: A FastAPI backend. It provides a RESTful interface for external integrations. It uses `psycopg3` for robust, async PostgreSQL persistence.

---

## 🛠️ SDK Usage

The `dmesh-sdk` is designed for flexibility, supporting multiple persistence modes via the repository pattern.

### 1. Local Persistency Mode (SQLite)

Perfect for local development or testing without external dependencies.

```python
import asyncio
from dmesh.sdk import create_dp, SQLiteRepository

async def main():
    # Initialize a local SQLite repository
    repo = SQLiteRepository("dmesh.db")
    
    # Create a Data Product specification
    spec = {
        "domain": "finance",
        "name": "ledger",
        "version": "1.0.0"
    }
    
    # Execute the operation (fully async)
    dp = await create_dp(repo, spec)
    print(f"Created Data Product: {dp.id} ({dp.domain})")

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Production-Like Persistency Mode (Docker/Postgres)

Leverages a high-performance PostgreSQL backend with connection pooling.

```python
import asyncio
from dmesh.sdk import create_dp
from dmesh.sdk.persistency.postgres import PostgresDataProductRepository
from psycopg_pool import AsyncConnectionPool

async def main():
    # Configure an asynchronous connection pool
    conn_str = "host=localhost port=5432 user=postgres password=postgres dbname=postgres"
    async with AsyncConnectionPool(conninfo=conn_str) as pool:
        # Initialize the Postgres repository adapter
        repo = PostgresDataProductRepository(pool)
        
        # Create Data Product
        dp = await create_dp(repo, {"domain": "marketing", "name": "analytics"})
        print(f"Persisted to Postgres: {dp.id}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 💻 CLI Usage

The `dmesh` CLI provides a powerful set of tools to manage your Data Mesh environment.

### Installation & Setup

Ensure you have [uv](https://github.com/astral-sh/uv) installed, then sync the workspace:

```bash
uv sync
```

### Quick start

samples folder provide a quick start script and data product and data contract sample yaml files

Execute it to see the CLI in action:
```bash
bash -x ./samples/dmesh-cli-smoke-test.sh
```

### Common Commands

**Initialize the local environment:**
```bash
uv run dmesh init --full
```

**Manage Data Products:**
```bash
# Register a Data Product from a YAML specification
uv run dmesh put dp path/to/spec.yaml

# List all registered Data Products
uv run dmesh list dps

# Get details of a specific Data Product
uv run dmesh get dp <id>
```

**Manage Data Contracts:**
```bash
# Register a Data Contract for a parent Data Product
uv run dmesh put dc path/to/contract.yaml --dp-id <dp-id>

# List Data Contracts for a product
uv run dmesh list dcs --dp-id <dp-id>
```

### Launching the API

Start the backend server locally using Uvicorn:

```bash
uv run uvicorn dmesh.api.main:app --reload
```

### 🌐 API Documentation

Once the server is running, you can explore and interact with the **interactive OpenAPI (Swagger) documentation**:

-   **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
-   **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

All endpoints are consistently namespaced (default: `/dmesh/`) and support full aliasing (e.g., `/dmesh/dp`, `/dmesh/dps`, or `/dmesh/data-product` are all valid).

---

## 🧪 Testing

Run the full unified test suite from the repository root:

```bash
# Run unit tests (logic & models)
uv run pytest tests/unit

# Run core sdk integration tests
uv run pytest tests/integration/sdk/test_sdk.py

# Run integration tests (requires docker-compose up -d)
uv run pytest tests/integration
```