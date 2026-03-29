"""Custom exceptions for the dm init command."""


class DmInitError(Exception):
    """Base exception for all dm init errors."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DockerNotAvailableError(DmInitError):
    """Raised when Docker is not installed or the Docker daemon is not running."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ImagePullError(DmInitError):
    """Raised when a Docker image pull fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ImageBuildError(DmInitError):
    """Raised when a Docker image build fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ContainerStartError(DmInitError):
    """Raised when a Docker container fails to start."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class HealthCheckTimeoutError(DmInitError):
    """Raised when the WS health check does not return 200 within the timeout."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ConfigWriteError(DmInitError):
    """Raised when the config file cannot be written."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ContainerStopError(DmInitError):
    """Raised when a container fails to stop or be removed."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class NetworkRemoveError(DmInitError):
    """Raised when the Docker network cannot be removed."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ConfigRemoveError(DmInitError):
    """Raised when the config file cannot be deleted."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class ImageRemoveError(DmInitError):
    """Raised when a Docker image cannot be removed."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
