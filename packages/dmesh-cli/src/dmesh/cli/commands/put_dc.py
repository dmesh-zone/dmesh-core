"""dm put dc subcommand — create or update a data contract."""
from pathlib import Path
from typing import Optional

import httpx
import typer
import yaml

from dmesh.cli.put.config_reader import ConfigReader
from dmesh.cli.put.errors import ConfigMalformedError, ConfigNotFoundError, DmPutError
from dmesh.cli.put.errors import FileNotFoundError as DmFileNotFoundError
from dmesh.cli.put.errors import YamlParseError

DEFAULT_VERSION = "v1.0.0"


def _read_yaml(path: Path) -> dict:
    if not path.exists():
        raise DmFileNotFoundError(f"File not found: {path}")
    try:
        return yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError as e:
        raise YamlParseError(f"Failed to parse YAML: {e}") from e


def _find_dp_id(ws_base_url: str, domain: str, name: str, version: str) -> str:
    try:
        resp = httpx.get(
            f"{ws_base_url}/dps",
            params={"domain": domain, "name": name, "version": version},
            timeout=30,
        )
    except httpx.RequestError as e:
        raise DmPutError(f"WS layer is unreachable: {e}") from e
    if resp.status_code != 200:
        raise DmPutError(f"WS layer returned HTTP {resp.status_code}")
    results = resp.json()
    if not results:
        raise DmPutError(f"No data product found for domain={domain} name={name} version={version}")
    return results[0]["id"]


def put_dc(
    path: Path = typer.Argument(..., help="Path to the ODCS data contract YAML file."),
    dp: Optional[Path] = typer.Option(None, "--dp", help="Path to the parent data product YAML file."),
    domain: Optional[str] = typer.Option(None, "--domain", help="Parent data product domain."),
    dp_name: Optional[str] = typer.Option(None, "--dp_name", help="Parent data product name."),
    version: Optional[str] = typer.Option(None, "--version", help="Parent data product version (default: v1.0.0)."),
) -> None:
    """Create or update a data contract YAML file in the data mesh."""
    try:
        dc_spec = _read_yaml(path)
        config = ConfigReader().read()
        ws = config.ws_base_url

        dc_id = dc_spec.get("id")

        # UPDATE path — dc has an id
        if dc_id:
            try:
                resp = httpx.put(
                    f"{ws}/dcs/{dc_id}",
                    json=dc_spec,
                    timeout=30,
                )
            except httpx.RequestError as e:
                raise DmPutError(f"WS layer is unreachable: {e}") from e
            if resp.status_code == 404:
                raise DmPutError(f"Data contract {dc_id} not found.")
            if resp.status_code == 422:
                raise DmPutError(f"Validation error: {resp.json().get('detail', '')}")
            if resp.status_code != 200:
                raise DmPutError(f"WS layer returned HTTP {resp.status_code}")
            typer.echo(resp.json().get("id", dc_id))
            return

        # CREATE path — resolve parent dp_id
        if dp is not None:
            dp_spec = _read_yaml(dp)
            # Handle both raw spec and DataProductResponse wrapper
            if "specification" in dp_spec and isinstance(dp_spec["specification"], dict):
                dp_spec = dp_spec["specification"]
            d = dp_spec.get("domain", "")
            n = dp_spec.get("name", "")
            v = dp_spec.get("version", DEFAULT_VERSION)
        elif domain and dp_name:
            d, n, v = domain, dp_name, version or DEFAULT_VERSION
        else:
            raise DmPutError("Provide --dp <dp.yaml> or --domain and --dp_name to identify the parent data product.")

        dp_id = _find_dp_id(ws, d, n, v)

        try:
            resp = httpx.post(
                f"{ws}/dps/{dp_id}/dcs",
                json=dc_spec,
                timeout=30,
            )
        except httpx.RequestError as e:
            raise DmPutError(f"WS layer is unreachable: {e}") from e
        if resp.status_code == 422:
            raise DmPutError(f"Validation error: {resp.json().get('detail', '')}")
        if resp.status_code != 201:
            raise DmPutError(f"WS layer returned HTTP {resp.status_code}")
        typer.echo(resp.json().get("id", ""))

    except (DmPutError, DmFileNotFoundError, YamlParseError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
    except (ConfigNotFoundError, ConfigMalformedError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
