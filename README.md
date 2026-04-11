# dmesh-core

A modern, high-performance toolkit for managing **Open Data Mesh** specifications, focusing on Data Products and Data Contracts. This repository provides a unified `uv` workspace for the core SDK, REST API, and CLI components.

## 🏗️ Architecture Overview

The project is structured as a modular Python workspace with a clear separation of concerns:

-   **`dmesh-sdk`**: The core logic layer. Provides CRUD operations for Open Data Product and Open Data Contract specifications through a repository factory pattern that supports in-memory (for testing) and PostgreSQL (for production) persistency.
-   **`dmesh-cli`**: A Typer-powered command-line interface for local-first development. It allows users to setup a local environment, manage specifications, and interact with PostgreSQL backend.
-   **`dmesh-api`**: A FastAPI backend. It provides a RESTful interface for external integrations. It uses `psycopg3` for robust, async PostgreSQL persistence.

---

## 🛠️ SDK Usage

The `dmesh-sdk` is built natively for asynchronous operations, supporting in-memory storage for testing and PostgreSQL for production.

#### Usage Example (PostgreSQL)

Before running it, run the PostgreSQL docker with following command:
```bash
docker-compose up -d
```

Also ensure your environment variables are set (either in a `.env` file or exported in your shell):

```env
DMESH_DB__HOST=localhost
DMESH_DB__PORT=5432
DMESH_DB__USER=postgres
DMESH_DB__PASSWORD=postgres
DMESH_DB__NAME=postgres
```

Run the code shown below as follows:

```shell
uv run python packages/dmesh-sdk/quickstart_postgres.py
```

```python
import asyncio
import selectors
from dmesh.sdk import AsyncSDK, RepositoryFactory, get_settings

async def main():
    # Load settings from config service
    settings = get_settings()

    # Initialize a PostgreSQL repository using settings
    factory = RepositoryFactory().create_from_settings(settings, db_type="postgres")
    
    # Use the SDK as an asynchronous context manager
    async with AsyncSDK(factory) as sdk:
        # Register a data product (idempotent)
        dp_spec = {
            "domain": "finance",
            "name": "ledger"
        }

        dp = await sdk.put_data_product(dp_spec)
        stored_dp = await sdk.get_data_product(dp['id'])
        print(f"Registered Data Product ID: {stored_dp['id']}")
        print(f"Data Product: {stored_dp}")
        dc_spec = {}
        dc = await sdk.put_data_contract(dc_spec, stored_dp['id'])
        stored_dc = await sdk.get_data_contract(dc['id'])
        print(f"Registered Data Contract ID: {stored_dc['id']}")
        print(f"Data Contract: {stored_dc}")

if __name__ == "__main__":
    # Ensure correct loop factory for Windows if needed, though run() usually handles it
    asyncio.run(main(), loop_factory=lambda: asyncio.SelectorEventLoop(selectors.SelectSelector()))
```

---

## ⚙️ Configuration Management

`dmesh-core` uses a hierarchical configuration system powered by `pydantic-settings`. It supports profiles, environment variable overrides, and `.env` files for secrets management.

### 📜 Configuration Directory
All base and profile-specific configurations reside in the `config/` directory:
- `config/base.toml`: Shared defaults for all environments.
- `config/{profile}.toml`: Overrides for a specific profile (e.g., `development.toml`, `docker.toml`).

> see examples/config/base.toml, examples/config/local_docker.toml for examples of config files.

### 🌍 Environment Selection
The active profile is selected using the `APP_ENV` environment variable:
```bash
# Select the 'local_docker' profile (will load config/local_docker.toml)
export APP_ENV="local_docker"
```

### 🔐 Secrets and .env Files
Secrets should be stored in `.env` files at the project root. The system loads them in the following order:
1. `.env.{APP_ENV}`: Profile-specific secrets (e.g., `.env.production`).
2. `.env`: Base/local secrets.

> see examples/.env.local_docker for an example of a .env file.

> [!IMPORTANT]
> `.env` and profile-specific `.env.*` files are gitignored by default to prevent accidental secret leakage, except for `.env.development`.

### 🔝 Priority Stack
Configuration is resolved using the following priority (highest to lowest):
1. **CLI Flags / Runtime Args**: Passed directly to the settings constructor.
2. **Environment Variables**: Prefixed with `DMESH_` (e.g., `DMESH_DB__PORT="5433"`).
3. **`.env.{profile}` file**
4. **`.env` file**
5. **`config/{profile}.toml`**
6. **`config/base.toml`**
7. **Code Defaults**

### 🛠️ Overriding via Environment Variables
You can override any setting using environment variables with the `DMESH_` prefix. For nested settings, use double underscores `__`:
```bash
export DMESH_DB__HOST="localhost"
export DMESH_DB__PORT="5432"
...
```

### 🐍 Usage in Code
The settings are validated at startup. Missing required secrets will cause the application to exit with an error.

```python
from dmesh.sdk.config import get_settings

# This will validate the full config and exit if secrets are missing
settings = get_settings()

print(f"Connecting to {settings.db.host}:{settings.db.port}")
```

---

## 💻 CLI Usage

The `dmesh` CLI provides a set of tools to manage your Data Mesh environment.

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

**Setup the local environment (starts infrastructure):**
```bash
uv run dmesh setup
```

**Force a clean environment (teardown + setup):**
```bash
uv run dmesh reset
```

**Tear down the environment (stops infrastructure):**
```bash
uv run dmesh teardown --full
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
uv run dmesh put dc path/to/contract.yaml --dp <dp-id>

# List Data Contracts for a product
uv run dmesh list dcs --dp <dp-id>
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

# Run integration tests (requires uv run dmesh setup)
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