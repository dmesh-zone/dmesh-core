"""ConfigRemover for deleting ~/.dm/config.yaml during deinit."""

from dm.init.config_writer import CONFIG_PATH
from dm.init.errors import ConfigRemoveError
from dm.init.feedback import Feedback


class ConfigRemover:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def remove(self) -> None:
        """Remove ~/.dm/config.yaml if it exists. The parent ~/.dm/ directory is preserved."""
        if not CONFIG_PATH.exists():
            self._feedback.step("Config file not found, skipping.")
            return

        self._feedback.step(f"Removing config file {CONFIG_PATH}...")
        try:
            CONFIG_PATH.unlink()
        except OSError:
            raise ConfigRemoveError(
                "Failed to remove config at '~/.dm/config.yaml'. Check file system permissions."
            )
        self._feedback.success("Config file removed.")
