import os
from unittest.mock import patch, AsyncMock
from contextlib import asynccontextmanager
from typer.testing import CliRunner
from dmesh.sdk import AsyncSDK
from dmesh.sdk.persistency.factory import RepositoryFactory

# Shared factory for test
test_factory = RepositoryFactory().create(db_type="memory")
test_service = AsyncSDK(test_factory)

from dmesh.cli.main import app

runner = CliRunner()

def _get_async_mock_service():
    """Create an async context manager that returns test_service"""
    @asynccontextmanager
    async def async_mock_service():
        yield test_service
    return async_mock_service()

@patch('dmesh.cli.commands.delete.get_service')
@patch('dmesh.cli.commands.get.get_service')
@patch('dmesh.cli.commands.list.get_service')
@patch('dmesh.cli.commands.put.get_service')
@patch('dmesh.cli.utils.get_service')
def test_cli_lifecycle(
    mock_utils_get_service,
    mock_put_get_service,
    mock_list_get_service,
    mock_get_get_service,
    mock_delete_get_service,
):
    # Setup all mocks to return the async context manager
    mock_utils_get_service.return_value = test_service
    mock_put_get_service.return_value = _get_async_mock_service()
    mock_list_get_service.return_value = _get_async_mock_service()
    mock_get_get_service.return_value = _get_async_mock_service()
    mock_delete_get_service.return_value = _get_async_mock_service()
    # 1. Setup
    result = runner.invoke(app, ["setup"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "Data mesh initialised and ready" in result.stdout
    
    # 2. Put DP
    spec_path = "test_dp.yaml"
    with open(spec_path, "w") as f:
        f.write("""
apiVersion: v1.0.0
domain: test-cli
name: my-product
version: 1.0.0
""")
    
    result = runner.invoke(app, ["put", "dp", spec_path])
    assert result.exit_code == 0
    dp_id = result.stdout.strip()
    
    # 3. List
    result = runner.invoke(app, ["list", "dps"])
    assert result.exit_code == 0
    assert "test-cli" in result.stdout
    assert "my-product" in result.stdout
    
    # 4. Get
    result = runner.invoke(app, ["get", "dp", dp_id])
    assert result.exit_code == 0
    assert "test-cli" in result.stdout
    
    # 5. Delete
    result = runner.invoke(app, ["delete", "dp", dp_id])
    assert result.exit_code == 0
    assert f"Data product {dp_id} deleted" in result.stdout
    
    # 6. Teardown
    result = runner.invoke(app, ["teardown"])
    assert result.exit_code == 0
    assert "removed" in result.stdout
    
    # Cleanup
    if os.path.exists(spec_path):
        os.remove(spec_path)
