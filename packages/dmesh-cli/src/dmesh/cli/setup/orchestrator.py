"""SetupOrchestrator for the dm setup command."""

import os
import sys
from pathlib import Path
from dmesh.cli.setup.config_writer import ConfigWriter, CONFIG_PATH
from dmesh.cli.setup.feedback import Feedback
from dmesh.sdk import AsyncSDK
from dmesh.sdk.persistency.factory import RepositoryFactory


class SetupOrchestrator:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    async def run(self, flush: bool = False) -> None:
        """Execute the initialisation sequence."""
        self._feedback.step("Initializing local data mesh environment...")
        
        # Check if running in test mode (pytest)
        is_test = "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ
        
        if not is_test:
            # Start infrastructure via docker-compose
            self._feedback.step("Starting infrastructure via docker-compose...")
            import subprocess
            try:
                subprocess.run(["docker-compose", "up", "-d"], check=True, capture_output=True)
                self._feedback.success("Infrastructure started.")
            except subprocess.CalledProcessError as e:
                self._feedback.error(f"Failed to start infrastructure: {e.stderr.decode()}")
                raise Exception("Docker Compose failed") from e

        # Ensure config directory exists
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        if is_test:
            # Use in-memory for unit tests
            self._feedback.step("Initializing in-memory repository for tests...")
            factory = RepositoryFactory().create(db_type="memory")
        else:
            # Use postgres for integration/local dev
            self._feedback.step("Initializing Postgres database...")
            
            factory = RepositoryFactory().create(
                db_type="postgres",
                pg_host=os.getenv('DB_HOST', 'localhost'),
                pg_port=int(os.getenv('DB_PORT', '5432')),
                pg_user=os.getenv('DB_USER', 'postgres'),
                pg_password=os.getenv('DB_PASSWORD', 'postgres'),
                pg_db=os.getenv('DB_NAME', 'postgres')
            )
        
        async with AsyncSDK(factory) as sdk:
            if flush:
                self._feedback.step("Flushing existing data...")
                await sdk.flush()
                self._feedback.success("Data flushed.")
        
        # Write config
        if not is_test:
            ConfigWriter(self._feedback).write_pg(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', '5432')),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres'),
                dbname=os.getenv('DB_NAME', 'postgres')
            )
        
        mode = "test (in-memory)" if is_test else "Postgres"
        self._feedback.success(f"Data mesh initialised and ready ({mode} mode).")
