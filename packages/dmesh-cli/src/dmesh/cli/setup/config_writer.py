"""ConfigWriter for persisting config/base.toml."""

from pathlib import Path
from typing import Optional

from dmesh.cli.setup.errors import ConfigWriteError
from dmesh.cli.setup.feedback import Feedback

PROJECT_CONFIG_PATH = Path("config/base.toml")


class ConfigWriter:
    def __init__(self, feedback: Feedback) -> None:
        self._feedback = feedback

    def write_pg(self, host, port, user, password, dbname, rest_persistency_proxy: bool = False, rest_persistency_proxy_uses_databricks_m2m: bool = False, rest_persistency_proxy_url: str = "http://0.0.0.0:8000", topology: str = "docker-postgres", filesystem_persistency: bool = False, data_products_filesystem_root: str = "tmp/data_products_filesystem_root", data_products_filesystem_extra_path: Optional[str] = None) -> None:
        """Write Postgres and SDK config to config/base.toml."""
        self._feedback.step(f"Writing configuration to {PROJECT_CONFIG_PATH}...")
        try:
            PROJECT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
            extra_path_str = f'\ndata_products_filesystem_extra_path = "{data_products_filesystem_extra_path}"' if data_products_filesystem_extra_path else ""
            toml_content = f"""[db]
host = "{host}"
port = {port}
user = "{user}"
password = "{password}"
name = "{dbname}"

[sdk]
topology = "{topology}"
rest_persistency_proxy = {"true" if rest_persistency_proxy else "false"}
rest_persistency_proxy_uses_databricks_m2m = {"true" if rest_persistency_proxy_uses_databricks_m2m else "false"}
rest_persistency_proxy_url = "{rest_persistency_proxy_url}"
filesystem_persistency = {"true" if filesystem_persistency else "false"}
data_products_filesystem_root = "{data_products_filesystem_root}"{extra_path_str}

[api.environments]
Dev = "{rest_persistency_proxy_url.rstrip('/')}/dmesh/discover"
QA = "{rest_persistency_proxy_url.rstrip('/')}/dmesh/discover"
Prod = "{rest_persistency_proxy_url.rstrip('/')}/dmesh/discover"
"""
            PROJECT_CONFIG_PATH.write_text(toml_content)
        except OSError:
            raise ConfigWriteError(f"Failed to write config to '{PROJECT_CONFIG_PATH}'.")
        self._feedback.success("Project configuration written.")
