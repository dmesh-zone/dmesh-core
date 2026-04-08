"""Container lifecycle management for the dm init command."""

import docker
import docker.errors

from dmesh.cli.init.errors import ContainerStartError, ImageBuildError, ImagePullError
from dmesh.cli.init.feedback import Feedback

DB_IMAGE = "dmesh-db:latest"
DB_CONTAINER = "dmesh-db"
DB_PORT = 5432

WS_IMAGE = "dmesh-ws:latest"
WS_CONTAINER = "dmesh-ws"
WS_PORT = 8000

NETWORK_NAME = "dmesh-net"
DB_ENVIRONMENT = {
    "POSTGRES_USER": "postgres",
    "POSTGRES_PASSWORD": "postgres",
    "POSTGRES_DB": "postgres",
}
import os
WS_BASE_PATH = os.environ.get("WS_BASE_PATH", "dmesh").strip("/")  # default base path — configurable via WS_BASE_PATH env var

WS_ENVIRONMENT = {
    "DB_HOST": "dmesh-db",
    "DB_PORT": "5432",
    "DB_USER": "postgres",
    "DB_PASSWORD": "postgres",
    "DB_NAME": "postgres",
    "WS_BASE_PATH": WS_BASE_PATH,
}


class ContainerManager:
    def __init__(self, feedback: Feedback) -> None:
        self.feedback = feedback
        self.client = docker.from_env()

    def ensure_network(self, name: str) -> None:
        """Create the Docker network if it does not already exist."""
        try:
            self.client.networks.get(name)
            self.feedback.step(f"Network {name} already exists.")
        except docker.errors.NotFound:
            self.feedback.step(f"Creating network {name}...")
            try:
                self.client.networks.create(name, driver="bridge")
            except docker.errors.DockerException as e:
                raise ContainerStartError(
                    f"Failed to create network {name}."
                ) from e
            self.feedback.success(f"Network {name} created.")

    def ensure_running(
        self,
        image: str,
        name: str,
        ports: dict,
        network: str | None = None,
        environment: dict | None = None,
    ) -> None:
        """Start container if not already running."""
        try:
            container = self.client.containers.get(name)
            if container.status == "running":
                self.feedback.step(f"{name} is already running.")
                return
            # Container exists but is stopped — restart it
            self.feedback.step(f"Starting container {name}...")
            try:
                container.start()
            except docker.errors.DockerException as e:
                raise ContainerStartError(
                    f"Container {name} failed to start. Run 'docker logs {name}' for details."
                ) from e
            self.feedback.success(f"Container {name} started.")
        except docker.errors.NotFound:
            # Container does not exist — run it
            self.feedback.step(f"Starting container {name}...")
            run_kwargs: dict = {"name": name, "ports": ports, "detach": True}
            if network is not None:
                run_kwargs["network"] = network
            if environment is not None:
                run_kwargs["environment"] = environment
            try:
                self.client.containers.run(image, **run_kwargs)
            except docker.errors.DockerException as e:
                raise ContainerStartError(
                    f"Container {name} failed to start. Run 'docker logs {name}' for details."
                ) from e
            self.feedback.success(f"Container {name} started.")

    def _pull_if_missing(self, image: str) -> None:
        """Pull the image only if it is not already present locally."""
        try:
            self.client.images.get(image)
        except docker.errors.ImageNotFound:
            self.feedback.step(f"Pulling image {image}...")
            try:
                self.client.images.pull(image)
            except docker.errors.DockerException as e:
                raise ImagePullError(
                    f"Failed to pull image {image}. Check your internet connection and try again."
                ) from e
            self.feedback.success(f"Image {image} pulled.")

    def build_if_missing(self, image: str, build_context_path: str) -> None:
        """Build the image from a local Dockerfile if it is not already present."""
        try:
            self.client.images.get(image)
            self.feedback.step(f"Image {image} already exists, skipping build.")
        except docker.errors.ImageNotFound:
            self.feedback.step(f"Building image {image}...")
            try:
                self.client.images.build(path=build_context_path, tag=image)
            except docker.errors.BuildError as e:
                raise ImageBuildError(
                    f"Failed to build image {image}. Check the Dockerfile and try again."
                ) from e
            self.feedback.success(f"Image {image} built.")
