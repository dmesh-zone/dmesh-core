#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"
WHEELS_DIR="$SCRIPT_DIR/wheels"

echo "Navigating to project root: $ROOT_DIR"
cd "$ROOT_DIR"

echo "Cleaning up old wheels..."
rm -rf "$WHEELS_DIR"
mkdir -p "$WHEELS_DIR"

# Also clean up project dist folder for safety
rm -rf "dist/"

echo "Building dmesh-sdk wheel..."
uv build --package dmesh-sdk --wheel

echo "Exporting dependencies to temporary requirements file..."
uv export --package dmesh-api --no-hashes --format requirements-txt --no-emit-project > "$SCRIPT_DIR/requirements.txt"

echo "Replacing workspace reference with the built wheel..."
SDK_WHEEL=$(ls dist/dmesh_sdk*.whl | head -n 1)
WHEEL_NAME=$(basename "$SDK_WHEEL")

# Copy only the SDK wheel
cp "$SDK_WHEEL" "$WHEELS_DIR/"

# Update requirements.txt to point to the local wheel instead of workspace path
sed -i.bak -e "s|-e ./packages/dmesh-sdk|./wheels/$WHEEL_NAME|" "$SCRIPT_DIR/requirements.txt"
rm "$SCRIPT_DIR/requirements.txt.bak"

echo "Success! The dmesh-sdk has been packaged into $WHEELS_DIR."
echo "Public dependencies will be installed from PyPI by Databricks."
echo "The requirements.txt is ready to be deployed."
