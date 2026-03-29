"""ConfigWriter for persisting ~/.dm/config.yaml."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

from dm.init.errors import ConfigWriteError
from dm.init.feedback import Feedback

CONFIG_PATH = Path.home() / ".dm" / "config.yaml"


@dataclass
class DmConfig:
    ws_base_url: Optional[str] = None
    sqlite_path: Optional[str] = None
    pg_host: Optional[str] = None
    pg_port: Optional[int] = None
    pg_user: Optional[str] = None
    pg_password: Optional[str] = None
    pg_db: Optional[str] = None


class ConfigWriter:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def write(self, config_dict: dict) -> None:
        """Write (or overwrite) ~/.dm/config.yaml with connection settings."""
        self._feedback.step("Writing configuration to ~/.dm/config.yaml...")
        try:
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with CONFIG_PATH.open("w") as f:
                yaml.dump(config_dict, f)
        except OSError:
            raise ConfigWriteError(
                "Failed to write config to '~/.dm/config.yaml'. Check file system permissions."
            )
        self._feedback.success("Configuration written.")

    def write_ws(self, ws_base_url: str) -> None:
        """Write ws config."""
        self.write({"ws": {"base_url": ws_base_url}})

    def write_sqlite(self, sqlite_path: str) -> None:
        """Write SQLite config."""
        self.write({"sqlite": {"path": sqlite_path}})

    def write_pg(self, host, port, user, password, dbname) -> None:
        """Write Postgres config."""
        self.write({
            "postgres": {
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "dbname": dbname
            }
        })
