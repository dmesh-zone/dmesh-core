#!/usr/bin/env bash

# Prevent the script from being sourced, which would cause `set -e` and `exit` to close the user's terminal.
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
  echo "Error: This script should not be sourced. Please run it directly using ./deploy-api-as-databricks-app.sh"
  return 1 2>/dev/null || exit 1
fi

set -e

# Navigate to the directory of this script (dmesh-api)
cd "$(dirname "$0")"

# Process arguments
if [ -z "$1" ]; then
  echo "Usage: ./deploy-api-as-databricks-app.sh <target>"
  echo "Targets:"
  echo "  mem      - Deploy using the in-memory configuration (app-mem.yaml)"
  echo "  lakebase - Deploy using the lakebase configuration (app-lakebase.yaml)"
  exit 1
fi

DEPLOY_TARGET="$1"

if [ "$DEPLOY_TARGET" != "mem" ] && [ "$DEPLOY_TARGET" != "lakebase" ]; then
  echo "Error: Invalid deployment target '$DEPLOY_TARGET'. Must be 'mem' or 'lakebase'."
  exit 1
fi

echo "=========================================="
echo " Preparing deployment for target: $DEPLOY_TARGET"
echo "=========================================="

APP_YAML_FILE="app-${DEPLOY_TARGET}.yaml"

if [ ! -f "$APP_YAML_FILE" ]; then
  echo "Error: $APP_YAML_FILE not found in dmesh-api directory!"
  exit 1
fi

# Copy the selected config to app.yaml so Databricks uses it
cp "$APP_YAML_FILE" app.yaml

if [ ! -f .env ]; then
  echo "Error: .env file not found in dmesh-api directory!"
  exit 1
fi

source .env

if [ -z "$DATABRICKS_EMAIL" ] || [ -z "$DB_PROFILE" ]; then
  echo "Error: Please ensure DATABRICKS_EMAIL and DB_PROFILE are set in your .env file."
  exit 1
fi

echo "=========================================="
echo " 1. Building SDK and requirements"
echo "=========================================="
./build-sdk-wheel.sh

echo "=========================================="
echo " 3. Syncing to Databricks Workspace"
echo "=========================================="
# Ensure app exists silently
if ! databricks apps get dmesh-api --profile "$DB_PROFILE" >/dev/null 2>&1; then
  echo "Creating new Databricks App: dmesh-api..."
  databricks apps create dmesh-api --profile "$DB_PROFILE"
fi

databricks sync . "/Workspace/Users/$DATABRICKS_EMAIL/dmesh-api" --profile "$DB_PROFILE" \
  --include "/requirements.txt" \
  --include "/wheels/**"

echo "=========================================="
echo " 4. Deploying Databricks App"
echo "=========================================="
databricks apps deploy dmesh-api --source-code-path "/Workspace/Users/$DATABRICKS_EMAIL/dmesh-api" --profile "$DB_PROFILE"

echo "Deployment complete! You can view the status in the Databricks UI."

# Clean up temporary config file
rm -f app.yaml
