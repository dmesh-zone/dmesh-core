"""ConfigWriter for persisting ~/.dm/config.yaml."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml

from dmesh.cli.init.errors import ConfigWriteError
from dmesh.cli.init.feedback import Feedback

CONFIG_PATH = Path.home() / ".dm" / "config.yaml"
PROJECT_CONFIG_PATH = Path("config/base.toml")

@dataclass
class DmConfig:
    ws_base_url: Optional[str] = None
    pg_host: Optional[str] = None
    pg_port: Optional[int] = None
    pg_user: Optional[str] = None
    pg_password: Optional[str] = None
    pg_db: Optional[str] = None


class ConfigWriter:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def write(self, config_dict: dict) -> None:
        """Write (or overwrite) ~/.dm/config.yaml and config/base.toml."""
        # 1. Write legacy YAML config
        self._feedback.step(f"Writing configuration to {CONFIG_PATH}...")
        try:
            CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            with CONFIG_PATH.open("w") as f:
                yaml.dump(config_dict, f)
        except OSError:
            raise ConfigWriteError(f"Failed to write config to '{CONFIG_PATH}'.")
        self._feedback.success("Legacy configuration written.")

        # 2. Write project-local TOML config (for get_settings support)
        self._feedback.step(f"Writing configuration to {PROJECT_CONFIG_PATH}...")
        try:
            PROJECT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            pg = config_dict.get("postgres", {})
            toml_content = f"""[db]
host = "{pg.get('host', 'localhost')}"
port = {pg.get('port', 5432)}
user = "{pg.get('user', 'postgres')}"
password = "{pg.get('password', 'postgres')}"
name = "{pg.get('dbname', 'postgres')}"
"""
            PROJECT_CONFIG_PATH.write_text(toml_content)
        except OSError:
            raise ConfigWriteError(f"Failed to write config to '{PROJECT_CONFIG_PATH}'.")
        self._feedback.success("Project configuration written.")

    def write_ws(self, ws_base_url: str) -> None:
        """Write ws config."""
        self.write({"ws": {"base_url": ws_base_url}})

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
