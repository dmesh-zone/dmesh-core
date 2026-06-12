#!/usr/bin/env bash
set -e

# Change to the script's directory
cd "$(dirname "$0")"

if [ -f .env ]; then
    echo "Loading environment variables from .env"
    export $(grep -v '^#' .env | xargs)
fi

if [ $# -ne 1 ]; then
    echo "Usage: $0 {sim|test|prod}"
    exit 1
fi

MODE=$1

# 0. Set the Version (read from pyproject.toml)
SDK_VERSION=$(grep -E '^version\s*=\s*".*"' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')

if [ -z "$SDK_VERSION" ]; then
    echo "Error: Could not extract version from pyproject.toml"
    exit 1
fi

echo "Detected SDK_VERSION=$SDK_VERSION"

# 1. Build the Package
echo "Cleaning old artifacts from ../../dist..."
rm -f ../../dist/dmesh_sdk-*
echo "Building the package..."
uv build

case "$MODE" in
    sim)
        echo "Running Local Verification (sim)..."
        # 2. Local Verification
        uv venv .test_venv
        source .test_venv/bin/activate
        uv pip install "../../dist/dmesh_sdk-${SDK_VERSION}-py3-none-any.whl"
        uv run --active python quickstart_memory.py
        echo "Simulation verification successful."
        ;;
    test)
        echo "Publishing to TestPyPI (test)..."
        if [ -z "$DMESH_TESTPYPI_TOKEN" ]; then
            echo "Error: DMESH_TESTPYPI_TOKEN environment variable is not set."
            exit 1
        fi
        
        # 3. Publish to TestPyPI
        # We use an array for the glob to avoid issues if files don't match, though with set -e it shouldn't fail the script if it expands correctly
        uv publish ../../dist/dmesh_sdk-${SDK_VERSION}* --publish-url https://test.pypi.org/legacy/ --token "$DMESH_TESTPYPI_TOKEN"
        
        echo "Verifying Published Package from TestPyPI..."
        # 4. Verify Published Package
        uv run --active --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ --with "dmesh-sdk==${SDK_VERSION}" --no-project -- python -c "import dmesh.sdk; print('SDK loaded:', dmesh.sdk.AsyncSDK)"
        echo "Test publishing and verification successful."
        echo "URL: https://test.pypi.org/project/dmesh-sdk/${SDK_VERSION}/"
        ;;
    prod)
        echo "Publishing to PyPI (prod)..."
        if [ -z "$DMESH_PYPI_TOKEN" ]; then
            echo "Error: DMESH_PYPI_TOKEN environment variable is not set."
            exit 1
        fi
        
        # 5. Official Release
        uv publish ../../dist/dmesh_sdk-${SDK_VERSION}* --token "$DMESH_PYPI_TOKEN"
        echo "Production release successful."
        echo "URL: https://pypi.org/project/dmesh-sdk/${SDK_VERSION}/"
        ;;
    *)
        echo "Invalid mode: $MODE"
        echo "Usage: $0 {sim|test|prod}"
        exit 1
        ;;
esac
