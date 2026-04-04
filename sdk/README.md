# Open Data Mesh Python SDK

A high-level Python SDK for managing Open Data Mesh resources (Data Products and Data Contracts). This SDK encapsulates all business logic, validation, and enrichment required to interact with an Open Data Mesh environment.

## Architecture Layers

This project is structured into the following decoupled layers:

1. **Python SDK (Core Logic)**: The foundation of the system. Contains models, validation, enrichment, and the `OpenDataMesh` interface which orchestrates all operations.
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
from open_data_mesh_sdk import OpenDataMesh
from open_data_mesh_sdk.persistency.sqlite import SQLiteRepository

# Initialize with a local SQLite database
repository = SQLiteRepository("odm.db")
sdk = OpenDataMesh(repository)

# Create a Data Product
# By default, create_dp returns the specification as a dictionary
dp_spec = {
    "domain": "sales",
    "name": "annual-revenue"
}
dp = sdk.create_dp(dp_spec)
print(f"Created Data Product ID: {dp['id']}")

# Create a Data Contract for the Data Product
# The SDK automatically handles Bitol ODCS 3.1.0 validation
dc_spec = {
    "dataProduct": "annual-revenue",
    "status": "proposed"
}
dc = sdk.create_dc(dc_spec, dp_id=dp['id'])
print(f"Created Data Contract ID: {dc['id']}")

# Partial update (Patch) a Data Contract
# Note: customProperties are appended during a patch
patch_spec = {
    "id": dc['id'],
    "status": "active",
    "customProperties": [{"property": "someProperty", "value": "someValue"}]
}
patched_dc = sdk.patch_dc(patch_spec)
print(f"New Status: {patched_dc['status']}")
```

## Error Handling

The SDK provides specific exceptions for validation errors:

```python
from open_data_mesh_sdk.core.exceptions import DataProductValidationError, DataContractValidationError

try:
    sdk.create_dp({"invalid": "property"})
except DataProductValidationError as e:
    print(f"Validation failed: {e}")
```

## Discovery

Search for resources across your mesh:

```python
# Discover all resources associated with a Data Product
results = sdk.discover(domain="sales", name="annual-revenue")
for item in results:
    print(f"Found {item.get('kind')}: {item.get('id')}")
```

## Documentation

- **SDK Interface**: [open_data_mesh_sdk.sdk](src/open_data_mesh_sdk/sdk.py)
- **Models**: [open_data_mesh_sdk.core.models](src/open_data_mesh_sdk/core/models.py)
- **Examples**: [examples/](examples/)
