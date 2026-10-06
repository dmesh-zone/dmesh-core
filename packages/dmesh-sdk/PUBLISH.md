# Publishing Data Mesh SDK

Instructions for building, testing locally, and publishing the `dmesh-sdk` package using the automated `publish.sh` script.

## 0. Set the Version

The SDK version is defined in `packages/dmesh-sdk/pyproject.toml`. Ensure it is incremented appropriately before publishing.

```toml
[project]
name = "dmesh-sdk"
version = "0.0.0"  # <--- Update this
```

## 1. Configure Credentials

The `publish.sh` script automatically reads environment variables from a `.env` file in the `packages/dmesh-sdk` directory. 

Create a `.env` file with your PyPI and TestPyPI tokens:

```bash
# packages/dmesh-sdk/.env
DMESH_TESTPYPI_TOKEN="your-testpypi-token"
DMESH_PYPI_TOKEN="your-pypi-token"
```

## 2. Using `publish.sh`

Navigate to the `dmesh-sdk` package directory and run the `publish.sh` script with one of the following modes:

```bash
cd packages/dmesh-sdk
./publish.sh {sim|test|prod}
```

### Modes

#### `sim` (Simulation / Local Verification)
Builds the package and runs a local verification script (`quickstart_memory.py`) in an isolated virtual environment (`.test_venv`) to ensure the built wheel functions correctly.

```bash
./publish.sh sim
```

#### `test` (TestPyPI Release)
Builds the package, publishes it to TestPyPI using `$DMESH_TESTPYPI_TOKEN`, and performs a verification check by downloading and loading the newly published package from TestPyPI.

```bash
./publish.sh test
```

#### `prod` (Production PyPI Release)
Builds the package and publishes it directly to the official PyPI registry using `$DMESH_PYPI_TOKEN`.

```bash
./publish.sh prod
```

> [!NOTE]
> Ensure you have the `uv` package manager installed, as the script relies heavily on it for building, virtual environment management, and publishing.
