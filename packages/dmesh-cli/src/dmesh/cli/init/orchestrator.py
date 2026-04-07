"""InitOrchestrator for the dm init command."""

import os
import sys
from pathlib import Path
from dmesh.cli.init.config_writer import ConfigWriter, CONFIG_PATH
from dmesh.cli.init.feedback import Feedback
from dmesh.sdk import DataMeshService
from dmesh.sdk.persistency.in_memory import InMemoryRepository


class InitOrchestrator:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def run(self, flush: bool = False) -> None:
        """Execute the initialisation sequence."""
        self._feedback.step("Initializing local data mesh environment...")
        
        # Ensure config directory exists
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if running in test mode (pytest)
        is_test = "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ
        
        if is_test:
            # Use in-memory for unit tests
            self._feedback.step("Initializing in-memory repository for tests...")
            repository = InMemoryRepository()
            service = DataMeshService(repository)
        else:
            # Use postgres for integration/local dev
            from dmesh.sdk.persistency.postgres import PostgresSyncRepository
            import psycopg_pool
            self._feedback.step("Initializing Postgres database...")
            conn_str = f"host={os.getenv('DB_HOST', 'localhost')} port={os.getenv('DB_PORT', '5432')} user={os.getenv('DB_USER', 'postgres')} password={os.getenv('DB_PASSWORD', 'postgres')} dbname={os.getenv('DB_NAME', 'postgres')}"
            pool = psycopg_pool.ConnectionPool(conn_str)
            repository = PostgresSyncRepository(pool)
            service = DataMeshService(repository)
        
        if flush:
            self._feedback.step("Flushing existing data...")
            service.flush()
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
