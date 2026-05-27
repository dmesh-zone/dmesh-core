import asyncio
import sys
import os
import pytest

# This must be done at the module level to ensure it happens before any event loop is created

# Automatically configure DOCKER_HOST for macOS users running Colima (to fix IDE test runs)
if sys.platform == 'darwin' and 'DOCKER_HOST' not in os.environ:
    colima_sock = os.path.expanduser('~/.colima/default/docker.sock')
    if os.path.exists(colima_sock):
        os.environ['DOCKER_HOST'] = f"unix://{colima_sock}"
        if 'TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE' not in os.environ:
            os.environ['TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE'] = '/var/run/docker.sock'

if sys.platform == 'win32':
    # On Windows, psycopg3 (and some other libs) require the SelectorEventLoop
    # instead of the default ProactorEventLoop to run async operations correctly.
    # We suppress the DeprecationWarning for WindowsSelectorEventLoopPolicy as it's 
    # currently the only way to satisfy psycopg3's requirements on Windows.
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Disable Ryuk on Windows by default as it often fails with port mapping errors
    if "TESTCONTAINERS_RYUK_DISABLED" not in os.environ:
        os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"

def pytest_addoption(parser):
    parser.addoption(
        "--external-db", action="store_true", default=False, help="Use external DB instead of testcontainers"
    )
    parser.addoption(
        "--run-perf", action="store_true", default=False, help="Run performance tests"
    )

def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-perf"):
        return
    skip_perf = pytest.mark.skip(reason="need --run-perf option to run")
    for item in items:
        if "performance" in item.keywords:
            item.add_marker(skip_perf)
