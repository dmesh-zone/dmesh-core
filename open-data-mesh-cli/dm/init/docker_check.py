"""Docker prerequisite checker for the dm init command."""

import docker

from dm.init.errors import DockerNotAvailableError
from dm.init.feedback import Feedback


class DockerPrerequisiteChecker:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def check(self) -> None:
        """Raises DockerNotAvailableError if Docker is absent or daemon is not running."""
        self._feedback.step("Checking Docker availability...")
        try:
            client = docker.from_env()
            client.ping()
        except FileNotFoundError:
            raise DockerNotAvailableError(
                "Docker is not installed. Please install Docker Desktop from "
                "https://docs.docker.com/get-docker/ and try again."
            )
        except docker.errors.DockerException:
            raise DockerNotAvailableError(
                "Docker daemon is not running. Please start Docker Desktop and try again."
            )
        self._feedback.success("Docker is available.")
