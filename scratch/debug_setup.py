import sys
from typer.testing import CliRunner
from dmesh.cli.main import app

def test_setup_simple():
    runner = CliRunner()
    print("\nRunning setup...")
    result = runner.invoke(app, ["setup"], catch_exceptions=False)
    print(f"Exit code: {result.exit_code}")
    print(f"Output: {result.stdout}")

if __name__ == "__main__":
    test_setup_simple()
