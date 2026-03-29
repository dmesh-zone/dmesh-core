"""Container stop and removal logic for the dm deinit command."""

import docker
import docker.errors
from docker.errors import DockerException

from dm.init.container_manager import DB_CONTAINER, NETWORK_NAME, WS_CONTAINER
from dm.init.errors import ContainerStopError, NetworkRemoveError
from dm.init.feedback import Feedback


class ContainerRemover:
    def __init__(self, feedback: Feedback) -> None:
        self.feedback = feedback
        self.client = docker.from_env()

    def stop_and_remove(self, name: str) -> None:
        """Stop and remove a container by name."""
        try:
            container = self.client.containers.get(name)
        except docker.errors.NotFound:
            self.feedback.step(f"{name} container not found, skipping.")
            return

        if container.status == "running":
            self.feedback.step(f"Stopping container {name}...")
            try:
                container.stop()
            except DockerException as e:
                raise ContainerStopError(
                    f"Failed to stop container {name}. Run 'docker rm -f {name}' to force removal."
                ) from e
            self.feedback.success(f"Container {name} stopped.")

        self.feedback.step(f"Removing container {name}...")
        try:
            container.remove()
        except DockerException as e:
            raise ContainerStopError(
                f"Failed to remove container {name}. Run 'docker rm -f {name}' to force removal."
            ) from e
        self.feedback.success(f"Container {name} removed.")

    def remove_network(self, name: str) -> None:
        """Remove a Docker network by name."""
        try:
            network = self.client.networks.get(name)
        except docker.errors.NotFound:
            self.feedback.step(f"Network {name} not found, skipping.")
            return

        self.feedback.step(f"Removing network {name}...")
        try:
            network.remove()
        except DockerException as e:
            raise NetworkRemoveError(
                f"Failed to remove network {name}. Run 'docker network rm {name}' to remove it manually."
            ) from e
        self.feedback.success(f"Network {name} removed.")
