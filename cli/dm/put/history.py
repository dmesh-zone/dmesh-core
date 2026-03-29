"""Manages ~/.dm/history.yaml — tracks last created/updated objects."""
from pathlib import Path
from typing import Optional

import yaml

HISTORY_PATH = Path.home() / ".dm" / "history.yaml"


def record_dp(dp_id: str, domain: str, name: str, version: str) -> None:
    """Append/update the last data product entry in history."""
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    history = _load()
    history["last_dp"] = {"id": dp_id, "domain": domain, "name": name, "version": version}
    with HISTORY_PATH.open("w") as f:
        yaml.dump(history, f)


def last_dp() -> Optional[dict]:
    """Return the last data product entry or None."""
    history = _load()
    return history.get("last_dp")


def record_dc(dc_id: str, domain: str, name: str, version: str) -> None:
    """Record the last created/updated data contract."""
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    history = _load()
    history["last_dc"] = {"id": dc_id, "domain": domain, "name": name, "version": version}
    with HISTORY_PATH.open("w") as f:
        yaml.dump(history, f)


def last_dc() -> Optional[dict]:
    """Return the last recorded data contract or None."""
    return _load().get("last_dc")


def _load() -> dict:
    if not HISTORY_PATH.exists():
        return {}
    try:
        return yaml.safe_load(HISTORY_PATH.read_text()) or {}
    except yaml.YAMLError:
        return {}
