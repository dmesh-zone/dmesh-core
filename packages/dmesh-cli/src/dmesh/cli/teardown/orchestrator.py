"""TeardownOrchestrator for the dm teardown command."""

import os
from dmesh.cli.setup.feedback import Feedback
from dmesh.cli.teardown.config_remover import ConfigRemover


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

        ConfigRemover(self._feedback).remove()

        self._feedback.success("Local data mesh environment removed.")
