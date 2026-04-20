# dmesh-sdk

![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Python Support](https://img.shields.io/badge/python-3.10%2B-blue)

A native asynchronous SDK, provided as a part of [dmesh-core](https://github.com/dmesh-zone/dmesh-core) for managing [open data product](https://bitol-io.github.io/open-data-product-standard/v1.0.0/) and [open data contract](https://bitol-io.github.io/open-data-contract-standard/v3.1.0/) standards. `dmesh-sdk` provides the core abstractions and persistence layers needed to implement the Open Data Mesh standard.

## 🚀 Key Features

*   **Async First**: Built from the ground up for high-performance asynchronous operations using `asyncio` and `psycopg3`.
*   **Idempotent Operations**: Safely publish and update data products and contracts.
*   **Validation**: Built-in JSON Schema validation for Data Product and Data Contract specifications.
*   **Pluggable Architecture**: Easily switch between storage backends (In-memory for testing, PostgreSQL for production).
*   **Factory-based Initialization**: Simplified setup for complex repository configurations.

## 📦 Installation

```bash
pip install dmesh-sdk
```

## 🛠️ Quick Start

### In-Memory persistency

```python
import asyncio
from dmesh.sdk import AsyncSDK, RepositoryFactory

async def main():
    # Initialize an In-Memory repository for testing
    factory = RepositoryFactory().create(db_type="memory")
    
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
    asyncio.run(main())    
```

```shell
Registered Data Product ID: ba781283-1f14-5db2-a3f3-ce330da2c6dd
Data Product: {'domain': 'finance', 'name': 'ledger', 'apiVersion': 'v1.0.0', 'kind': 'DataProduct', 'version': 'v1.0.0', 'status': 'draft', 'id': 'ba781283-1f14-5db2-a3f3-ce330da2c6dd'}
Registered Data Contract ID: b9ee4bd2-205d-5eb8-8e13-1f9ee1f6ea26
Data Contract: {'id': 'b9ee4bd2-205d-5eb8-8e13-1f9ee1f6ea26', 'apiVersion': 'v3.1.0', 'kind': 'DataContract', 'version': 'v1.0.0', 'status': 'draft', 'dataProduct': 'ledger', 'domain': 'finance'}
```

### Postgres persistency

To use the PostgreSQL backend, you need a running database.

#### Option 1: Fast Docker Run (Simplest)
Run a standalone Postgres instance:

```bash
docker run --name dmesh-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres -p 5432:5432 -d postgres:16
```

#### Option 2: Docker Compose (Monorepo)
If you have the full [dmesh-core](https://github.com/dmesh-zone/dmesh-core) repository, you can use the included `docker-compose.yml`:

```bash
docker-compose up -d db
```

#### Configuration
Before running the code below, ensure your environment variables are set (either in a `.env` file or exported in your shell):

```env
DMESH_DB__HOST=localhost
DMESH_DB__PORT=5432
DMESH_DB__USER=postgres
DMESH_DB__PASSWORD=postgres
DMESH_DB__NAME=postgres
```

```python
import asyncio
import selectors
from dmesh.sdk import AsyncSDK, RepositoryFactory, get_settings

async def main():
    # Load settings from config service
    settings = get_settings()

    # Initialize an In-Memory repository for testing
    factory = RepositoryFactory().create_from_settings(db_type="postgres", settings=settings)
    
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





## 📖 Related Projects

*   **dmesh-cli**: Command-line interface for managing your data mesh.
*   **dmesh-api**: REST API (FastAPI based) server for data mesh orchestration.
*   **dmesh-viewer**: Web-based interface for data mesh visualization.

## 📄 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](https://github.com/dmesh-zone/dmesh-core/blob/main/LICENSE) file for details.
