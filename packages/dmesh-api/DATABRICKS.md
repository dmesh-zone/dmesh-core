# Deploying `dmesh-api` to Databricks Apps

To deploy the `dmesh-api` (which is a FastAPI application) as a Databricks App, you can use the Databricks Apps feature. Since your project uses FastAPI and `uvicorn`, the process is quite straightforward, though you'll need to account for how local workspace dependencies are structured.

Here are the steps to get it deployed:

## 1. Review the `app.yaml` Configuration File

The `app.yaml` file is already provided in the root of the `dmesh-api` package. This file tells Databricks what command to run to start your server. 

```yaml
# packages/dmesh-api/app.yaml
command:
  - "python"
  - "-m"
  - "uvicorn"
  - "dmesh.api.main:app"
  - "--host"
  - "0.0.0.0"
  - "--port"
  - "${DATABRICKS_APP_PORT}"
env:
  - name: "LOG_LEVEL"
    value: "INFO"
# Add any other required environment variables here
```

> [!NOTE]
> Databricks automatically injects the correct port via the `${DATABRICKS_APP_PORT}` environment variable, so it's critical to bind `uvicorn` to it.

## 2. Handle the Local `dmesh-sdk` Dependency

Currently, `packages/dmesh-api/pyproject.toml` references `dmesh-sdk` as a local workspace dependency (`dmesh-sdk = { workspace = true }`). When you deploy code to a Databricks App, Databricks essentially runs a standard `pip install` on your source directory.

If you upload the `packages/dmesh-api` directory as is, the deployment will fail because it won't be able to resolve the local `dmesh-sdk` package. Furthermore, it's highly recommended to package all dependencies as wheels to guarantee reproducible deployments and avoid downloading packages during the Databricks deployment process.

1. **Run the Build Script:**
   Navigate to the `packages/dmesh-api` directory and execute the `build-sdk-wheel.sh` script. This script will:
   - Build the `dmesh-sdk` wheel.
   - Export all of `dmesh-api`'s dependencies.
   - Download and build wheels for **all** dependencies into the `wheels` directory.
   - Automatically generate a `requirements.txt` that instructs Databricks to install directly from the `wheels` directory without connecting to PyPI.
   
   ```bash
   cd packages/dmesh-api
   ./build-sdk-wheel.sh
   ```

2. **Verify `requirements.txt`:**
   After the script completes, you should have a `requirements.txt` that starts with `--no-index` and `--find-links ./wheels`, followed by all dependency names.

## 3. Deploy via Databricks CLI

You must have the Databricks CLI installed and authenticated to your workspace to deploy the app.

### Prerequisites

If you don't have the Databricks CLI installed, you can install it on macOS using Homebrew:
```bash
brew tap databricks/tap
brew install databricks
```
*(Alternatively, you can use: `curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/setup.sh | sh`)*

Authenticate to your workspace:

We strongly recommend using **OAuth (User-to-Machine)** rather than a Personal Access Token (PAT) to ensure you have the correct workspace permissions for file syncing.

```bash
# Login via browser (recommended)
databricks auth login --host https://<your-databricks-workspace-url>
```
> [!NOTE]
> The `auth login` command will output a profile name when successful (e.g., `Profile dbc-XXXX was successfully saved`). Note this profile name, as you'll need to append `--profile <your-profile-name>` to subsequent commands if it differs from your default profile.

### Deployment

Databricks Apps deployment requires syncing your local source code to a Databricks Workspace folder before deploying.

Once your dependencies are resolvable and the CLI is ready, follow these steps to deploy:

```bash
# First, create a .env file with your variables if you haven't already
# DATABRICKS_EMAIL="your-databricks-email"
# DB_PROFILE="<your-databricks-profile>"

# Load variables from the .env file
source .env

# 1. Create the app entity in Databricks (only needed the first time)
databricks apps create dmesh-api --profile $DB_PROFILE

# 2. Sync your local files to a folder in your Databricks workspace
# We use --include flags to ensure requirements and wheels are not ignored by .gitignore
databricks sync . /Workspace/Users/$DATABRICKS_EMAIL/dmesh-api --profile $DB_PROFILE \
  --include "/requirements.txt" \
  --include "/wheels/**"

# 3. Deploy the source code from that workspace path
databricks apps deploy dmesh-api --source-code-path /Workspace/Users/$DATABRICKS_EMAIL/dmesh-api --profile $DB_PROFILE
```

Alternatively, if you use **Databricks Asset Bundles (DABs)**, you can integrate this into your existing `databricks.yml` instead of deploying manually.
