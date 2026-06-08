"""ConfigRemover for deleting config/base.toml and cleaning up legacy ~/.dm/config.yaml."""

from pathlib import Path

from dmesh.cli.setup.errors import ConfigRemoveError
from dmesh.cli.setup.feedback import Feedback
from dmesh.cli.setup.config_writer import PROJECT_CONFIG_PATH

LEGACY_CONFIG_PATH = Path.home() / ".dmesh" / "config.yaml"

class ConfigRemover:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def remove(self) -> None:
        """Remove config/base.toml if it exists. Silently cleans up legacy config.yaml."""
        
        # Silently clean up legacy yaml if it exists
        if LEGACY_CONFIG_PATH.exists():
            try:
                LEGACY_CONFIG_PATH.unlink()
            except OSError:
                pass # Ignore errors for legacy cleanup
                
        if not PROJECT_CONFIG_PATH.exists():
            self._feedback.step(f"Config file {PROJECT_CONFIG_PATH} not found, skipping.")
            return

        self._feedback.step(f"Removing config file {PROJECT_CONFIG_PATH}...")
        try:
            PROJECT_CONFIG_PATH.unlink()
        except OSError:
            raise ConfigRemoveError(
                f"Failed to remove config at '{PROJECT_CONFIG_PATH}'. Check file system permissions."
            )
        self._feedback.success("Config file removed.")
