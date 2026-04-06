"""ImageRemover for the dm deinit --full command."""

import docker
import docker.errors

from dmesh.cli.init.errors import ImageRemoveError
from dmesh.cli.init.feedback import Feedback


class ImageRemover:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback
        self._client = docker.from_env()

    def remove_image(self, image: str) -> None:
        """Remove a Docker image by tag and its underlying image ID if untagged."""
        try:
            self._client.images.get(image)
        except docker.errors.ImageNotFound:
            self._feedback.step(f"Image {image} not found, skipping.")
            return

        self._feedback.step(f"Removing image {image}...")
        try:
            self._client.images.remove(image, force=True)
        except docker.errors.DockerException as e:
            raise ImageRemoveError(
                f"Failed to remove image {image}. Run 'docker rmi {image}' to remove it manually."
            ) from e
        self._feedback.success(f"Image {image} removed.")

    def prune_dangling(self) -> None:
        """Remove all untagged (<none>:<none>) images left behind by builds."""
        untagged = [
            img for img in self._client.images.list(all=True)
            if not img.tags
        ]
        for img in untagged:
            try:
                self._client.images.remove(img.id, force=True)
            except docker.errors.DockerException:
                pass
