"""Resolves the Docker build context paths for bundled images."""

import importlib.resources
from contextlib import contextmanager
from pathlib import Path
from typing import Generator


@contextmanager
def db_build_context() -> Generator[str, None, None]:
    """Yield the filesystem path to the dmesh-db build context directory."""
    pkg = importlib.resources.files("dm.docker.dmesh-db")
    with importlib.resources.as_file(pkg) as ctx_path:
        yield str(ctx_path)


@contextmanager
def ws_build_context() -> Generator[str, None, None]:
    """Yield the filesystem path to the dmesh-ws build context directory."""
    pkg = importlib.resources.files("dm.docker.dmesh-ws")
    with importlib.resources.as_file(pkg) as ctx_path:
        yield str(ctx_path)
