"""Reads ~/.dm/config.yaml and returns a DmConfig."""
import yaml

from dmesh.cli.init.config_writer import CONFIG_PATH, DmConfig
from dmesh.cli.put.errors import ConfigMalformedError, ConfigNotFoundError


class ConfigReader:
    def read(self) -> DmConfig:
        """Read ~/.dm/config.yaml and return DmConfig.

        Raises:
            ConfigNotFoundError: if CONFIG_PATH does not exist.
            ConfigMalformedError: if config are absent or blank.
        """
        if not CONFIG_PATH.exists():
            raise ConfigNotFoundError(
                "Config file not found. Run `dm init` first."
            )
        raw = yaml.safe_load(CONFIG_PATH.read_text())
        if not isinstance(raw, dict):
            raise ConfigMalformedError("Config is malformed.")

        base_url = raw.get("ws", {}).get("base_url")
        pg = raw.get("postgres", {})
        
        if not base_url and not pg:
            raise ConfigMalformedError(
                "Config is malformed: no repository configured. Run `dm init` to reconfigure."
            )
        return DmConfig(
            ws_base_url=base_url, 
            pg_host=pg.get("host"),
            pg_port=pg.get("port"),
            pg_user=pg.get("user"),
            pg_password=pg.get("password"),
            pg_db=pg.get("dbname"),
        )
