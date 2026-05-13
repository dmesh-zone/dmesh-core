# Publishing Data Mesh SDK

Instructions for building, testing locally, and publishing the `dmesh-sdk` package.

## 0. Set the Version

The version is defined in `packages/dmesh-sdk/pyproject.toml`. Ensure it is incremented before building.

```toml
[project]
name = "dmesh-sdk"
version = "0.1.1"  # <--- Update this
```

For the following commands, set an environment variable to avoid hardcoding:

**Windows (PowerShell):**
```powershell
$env:SDK_VERSION = "0.1.1"
```

**Linux / macOS:**
```bash
export SDK_VERSION="0.1.1"
```

## 1. Build the Package

From the package directory:

```bash
cd packages/dmesh-sdk
uv build
```

The build artifacts will be in `../../dist/` (relative to `packages/dmesh-sdk`).

## 2. Local Verification

### Create and Activate Test Environment

**Windows (PowerShell):**
```powershell
uv venv .test_venv
.test_venv\Scripts\activate
```

**Linux / macOS:**
```bash
uv venv .test_venv
source .test_venv/bin/activate
```

### Install and Test

**Windows (PowerShell):**
```powershell
uv pip install "../../dist/dmesh_sdk-${env:SDK_VERSION}-py3-none-any.whl"
uv run --active python quickstart_memory.py
```

**Linux / macOS:**
```bash
uv pip install "../../dist/dmesh_sdk-${SDK_VERSION}-py3-none-any.whl"
uv run --active python quickstart_memory.py
```

## 3. Publish to TestPyPI

**Windows (PowerShell):**
```powershell
$env:DMESH_TESTPYPI_TOKEN = "your-testpypi-token"
uv publish "../../dist/dmesh_sdk-${env:SDK_VERSION}*" --publish-url https://test.pypi.org/legacy/ --token $env:DMESH_TESTPYPI_TOKEN
```

**Linux / macOS:**
```bash
export DMESH_TESTPYPI_TOKEN="your-testpypi-token"
uv publish "../../dist/dmesh_sdk-${SDK_VERSION}*" --publish-url https://test.pypi.org/legacy/ --token $DMESH_TESTPYPI_TOKEN
```

## 4. Verify Published Package

```bash
# Windows (PowerShell)
uv run --active --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --with "dmesh-sdk==${env:SDK_VERSION}" --no-project -- python -c "import dmesh.sdk; print('SDK loaded:', dmesh.sdk.AsyncSDK)"

# Linux / macOS
uv run --active --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --with "dmesh-sdk==${SDK_VERSION}" --no-project -- python -c "import dmesh.sdk; print('SDK loaded:', dmesh.sdk.AsyncSDK)"
```

## 5. Official Release

Once verified, publish to the main PyPI:

**Windows (PowerShell):**
```powershell
$env:DMESH_PYPI_TOKEN = "your-pypi-token"
uv publish "../../dist/dmesh_sdk-${env:SDK_VERSION}*" --token $env:DMESH_PYPI_TOKEN
```

**Linux / macOS:**
```bash
export DMESH_PYPI_TOKEN="your-pypi-token"
uv publish "../../dist/dmesh_sdk-${SDK_VERSION}*" --token $DMESH_PYPI_TOKEN
```
