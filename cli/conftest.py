import os
import sys
from pathlib import Path

# Disable Ryuk reaper container (required on Windows and in CI environments
# where the Ryuk sidecar cannot bind its port).
os.environ.setdefault("TESTCONTAINERS_RYUK_DISABLED", "true")

# Make the WS app importable as `app.*` in tests
_ws_app_path = Path(__file__).parent / "dm" / "docker" / "open-data-mesh-ws"
if str(_ws_app_path) not in sys.path:
    sys.path.insert(0, str(_ws_app_path))
