# dmesh-core

A modern, high-performance toolkit for managing **Open Data Mesh** specifications, focusing on Data Products and Data Contracts. This repository provides a unified `uv` workspace for the core SDK, REST API, and CLI components.

## 🏗️ Architecture Overview

The project is structured as a modular Python workspace with a clear separation of concerns:

-   **`dmesh-sdk`**: The core logic layer. Provides CRUD operations for Open Data Product and Open Data Contract specifications through a repository factory pattern that supports in-memory (for testing) and PostgreSQL (for production) persistency.
-   **`dmesh-cli`**: A Typer-powered command-line interface for local-first development. It allows users to initialize a local environment, manage specifications, and interact with PostgreSQL backend.
-   **`dmesh-api`**: A FastAPI backend. It provides a RESTful interface for external integrations. It uses `psycopg3` for robust, async PostgreSQL persistence.

---

## 🛠️ SDK Usage

The `dmesh-sdk` uses a repository factory pattern for flexible persistency configuration, supporting in-memory storage for testing and PostgreSQL for production.

### 1. In-Memory Persistency Mode (Testing)

Perfect for unit tests and isolated development without external dependencies.

```python
import asyncio
from dmesh.sdk import create_dp
from dmesh.sdk.persistency.factory import RepositoryFactory

async def main():
    # Create an in-memory repository factory
    factory = RepositoryFactory().create("memory")
    repo = factory.get_data_product_repository()
    
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

### 2. Production PostgreSQL Persistency Mode

Leverages a high-performance PostgreSQL backend with connection pooling.

```python
import asyncio
from dmesh.sdk import create_dp
from dmesh.sdk.persistency.factory import RepositoryFactory

async def main():
    # Create a PostgreSQL repository factory
    factory = RepositoryFactory().create(
        "postgres",
        pg_host="localhost",
        pg_port=5432,
        pg_user="postgres",
        pg_password="postgres",
        pg_db="postgres"
    )
    repo = factory.get_data_product_repository()
    
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

examples folder provide a quick start script and data product and data contract sample yaml files

Execute it to see the CLI in action (Linux/MacOS):
```bash
bash -x ./examples/dmesh-cli-smoke-test.sh
```

On Windows (PowerShell):
```powershell
.\examples\dmesh-cli-smoke-test.ps1
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

### VSCode Setup

The project includes VSCode configuration (`.vscode/settings.json`) that automatically detects uv's virtual environment:

- **Linux/macOS**: Uses `.venv/bin/python`
- **Windows**: VSCode auto-detects `.venv\Scripts\python.exe`

**For Windows users**: If VSCode doesn't automatically detect the correct interpreter, update `.vscode/settings.json`:
```json
"python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
"python.testing.pytestPath": "${workspaceFolder}/.venv/Scripts/pytest.exe"
```

VSCode will automatically discover and run tests from the Testing panel once the workspace is opened.