import os
from typer.testing import CliRunner
from dm.main import app
from dm.init.config_writer import CONFIG_PATH

runner = CliRunner()

def test_cli_lifecycle():
    # 1. Init
    result = runner.invoke(app, ["init"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "Data mesh initialised and ready" in result.stdout
    assert CONFIG_PATH.exists()
    
    # 2. Put DP
    # Create a dummy spec
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
    
    # 6. Deinit
    result = runner.invoke(app, ["deinit"])
    assert result.exit_code == 0
    assert "removed" in result.stdout
    assert not CONFIG_PATH.exists()
    
    # Cleanup
    if os.path.exists(spec_path):
        os.remove(spec_path)
