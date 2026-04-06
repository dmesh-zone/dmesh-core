"""DeinitOrchestrator for the dm deinit command."""

import os
from dmesh.cli.init.config_writer import CONFIG_PATH
from dmesh.cli.init.feedback import Feedback


class DeinitOrchestrator:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def run(self, full: bool = False) -> None:
        """Execute the deinitialisation sequence."""
        self._feedback.step("Removing local data mesh environment...")
        
        db_path = CONFIG_PATH.parent / "odm.db"
        
        if db_path.exists():
            self._feedback.step(f"Removing SQLite database at {db_path}...")
            os.remove(db_path)
            self._feedback.success("Database removed.")
            
        if CONFIG_PATH.exists():
            self._feedback.step(f"Removing configuration at {CONFIG_PATH}...")
            os.remove(CONFIG_PATH)
            self._feedback.success("Configuration removed.")
            
        self._feedback.success("Local data mesh environment removed.")
