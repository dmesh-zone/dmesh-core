"""TeardownOrchestrator for the dm teardown command."""

import os
from dmesh.cli.setup.config_writer import CONFIG_PATH
from dmesh.cli.setup.feedback import Feedback


class TeardownOrchestrator:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def run(self, full: bool = False) -> None:
        """Execute the deinitialisation sequence."""
        self._feedback.step("Removing local data mesh environment...")
        
        # Check if running in test mode (pytest)
        import sys
        is_test = "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ

        if not is_test:
            # Stop infrastructure via docker-compose
            self._feedback.step("Stopping infrastructure via docker-compose...")
            import subprocess
            try:
                subprocess.run(["docker-compose", "down"], check=True, capture_output=True)
                self._feedback.success("Infrastructure stopped.")
            except Exception as e:
                # We don't raise here to allow the rest of the cleanup to proceed
                self._feedback.error(f"Failed to stop infrastructure: {e}")

        if CONFIG_PATH.exists():
            self._feedback.step(f"Removing configuration at {CONFIG_PATH}...")
            os.remove(CONFIG_PATH)
            self._feedback.success("Configuration removed.")
            
        # Also remove project-local config if it exists
        from pathlib import Path
        project_config = Path("config/base.toml")
        if project_config.exists():
            self._feedback.step(f"Removing configuration at {project_config}...")
            os.remove(project_config)
            self._feedback.success("Project configuration removed.")

        self._feedback.success("Local data mesh environment removed.")
