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
# First, create a .env file with your variables if you haven't already
export DATABRICKS_WORKSPACE_URL="https://<your-databricks-workspace-url>"
# Login via browser (recommended)
databricks auth login --host $DATABRICKS_WORKSPACE_URL
```
> [!NOTE]
> The `auth login` command will output a profile name when successful (e.g., `Profile dbc-XXXX was successfully saved`). Note this profile name, as you'll need to append `--profile <your-profile-name>` to subsequent commands if it differs from your default profile.

### Deployment

To streamline the deployment process, we have provided an automated deployment script `deploy-api-as-databricks-app.sh`.

### Prerequisites

Ensure the following variables are set in your `.env` file within the `dmesh-api` directory:
```bash
DATABRICKS_EMAIL="your-databricks-email"
DB_PROFILE="<your-databricks-profile>"
```

### Deploying

Simply execute the deployment script. It will automatically build the `dmesh-sdk` wheel, copy it to the `dmesh-api` workspace, sync the files to Databricks, and trigger the App deployment.

```bash
./deploy-api-as-databricks-app.sh
```

## Troubleshooting

### `401 Unauthorized` on Programmatic Access (Service Principals)

If you have deployed the Databricks App but programmatic requests via your Service Principal are returning `401 Unauthorized`, it is highly likely that the Service Principal has not been properly granted the `CAN_USE` permission on the Databricks App itself.

The Databricks UI can sometimes be misleading. It's best to verify and grant permissions using the Databricks CLI.

#### 1. Check Current Permissions

You can view the actual Access Control List (ACL) for the app using the `get-permissions` command.

```bash
# Verify the current permissions on the dmesh-api app
databricks apps get-permissions dmesh-api --profile <your-databricks-profile>
```

If your Service Principal's UUID (e.g., `967ff765-514c-4024-8758-ae5087507412`) is not listed in the JSON response under `access_control_list`, it does not have permission to call the app.

#### 2. Grant `CAN_USE` to the Service Principal

To explicitly grant the `CAN_USE` permission to a Service Principal, you must use the `update-permissions` command with a JSON payload.

1. Create a file named `update_perms.json` containing the permission update for your Service Principal's UUID:

```json
{
  "access_control_list": [
    {
      "service_principal_name": "<YOUR-SERVICE-PRINCIPAL-UUID>",
      "permission_level": "CAN_USE"
    }
  ]
}
```

2. Apply the permissions:

```bash
databricks apps update-permissions dmesh-api --json @update_perms.json --profile $DB_PROFILE
```

3. Wait 1-2 minutes for the permissions to propagate across the Databricks infrastructure, then test your programmatic access again. You can safely delete `update_perms.json` once done.
