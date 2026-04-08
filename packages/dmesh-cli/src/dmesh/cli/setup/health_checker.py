"""Health checker for the dm init command."""

import time

import httpx

from dmesh.cli.init.errors import HealthCheckTimeoutError
from dmesh.cli.init.feedback import Feedback

from dmesh.cli.init.container_manager import WS_BASE_PATH
WS_HEALTH_URL = f"http://localhost:8000/{WS_BASE_PATH}/health"
HEALTH_CHECK_TIMEOUT = 30  # seconds


class HealthChecker:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def wait_until_healthy(self, url: str, timeout: int = 30) -> None:
        """Poll url every second until 200 OK or timeout. Raises HealthCheckTimeoutError."""
        self._feedback.step("Waiting for WS service to become healthy...")
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                response = httpx.get(url)
                if response.status_code == 200:
                    self._feedback.success("WS service is healthy.")
                    return
            except Exception:
                pass
            time.sleep(1)
        raise HealthCheckTimeoutError(
            "The WS service did not become healthy within 30 seconds. "
            "Run 'docker logs dmesh-ws' for details."
        )
