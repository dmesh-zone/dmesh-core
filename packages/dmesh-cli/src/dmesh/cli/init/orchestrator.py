"""InitOrchestrator for the dm init command."""

import os
from pathlib import Path
from dmesh.cli.init.config_writer import ConfigWriter, CONFIG_PATH
from dmesh.cli.init.feedback import Feedback
from dmesh.sdk import DataMeshService, SQLiteRepository


class InitOrchestrator:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def run(self, flush: bool = False) -> None:
        """Execute the initialisation sequence."""
        self._feedback.step("Initializing local data mesh environment...")
        
        # Ensure config directory exists
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        db_path = CONFIG_PATH.parent / "dmesh.db"
        
        # Initialize SQLite repository (this creates the tables)
        self._feedback.step(f"Initializing SQLite database at {db_path}...")
        repository = SQLiteRepository(str(db_path))
        service = DataMeshService(repository)
        
        if flush:
            self._feedback.step("Flushing existing data...")
            service.flush()
            self._feedback.success("Data flushed.")

        # Write config. We'll store the DB path in the config.
        # For now, let's keep it simple and just store the DB path.
        ConfigWriter(self._feedback).write_sqlite(str(db_path))
        
        self._feedback.success("Data mesh initialised and ready (SQLite mode).")
