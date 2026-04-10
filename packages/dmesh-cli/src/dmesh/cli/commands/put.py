"""dm put command group."""
from pathlib import Path
from typing import Optional
import uuid

import typer
import yaml

from dmesh.cli.put.errors import DmPutError, ConfigMalformedError, ConfigNotFoundError
from dmesh.cli.put.errors import FileNotFoundError as DmFileNotFoundError
from dmesh.cli.put.errors import YamlParseError
from dmesh.cli.put.history import record_dp, record_dc
from dmesh.cli.utils import get_service

app = typer.Typer(no_args_is_help=True)


def read_yaml_spec(path: Path) -> dict:
    """Read and parse a YAML file into a dict.

    Raises:
        dm.put.errors.FileNotFoundError: if the file does not exist.
        YamlParseError: if the file is not valid YAML.
    """
    if not path.exists():
        raise DmFileNotFoundError(f"File not found: {path}")
    try:
        return yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError as e:
        raise YamlParseError(f"Failed to parse YAML: {e}") from e


@app.command("dp")
def dp(
    path: Path = typer.Argument(..., help="Path to the ODPS data product YAML file."),
) -> None:
    """Publish a data product YAML file to the data mesh."""
    try:
        spec = read_yaml_spec(path)
        service = get_service()
        dp_obj = service.put_data_product(spec)
        record_dp(
            dp_id=dp_obj.id,
            domain=dp_obj.domain,
            name=dp_obj.name,
            version=dp_obj.version,
        )
        typer.echo(dp_obj.id)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command("dc")
def dc(
    path: Path = typer.Argument(..., help="Path to the ODCS data contract YAML file."),
    dp: Optional[str] = typer.Option(None, "--dp", help="Path to or ID of the parent data product."),
    domain: Optional[str] = typer.Option(None, "--domain", help="Parent data product domain."),
    dp_name: Optional[str] = typer.Option(None, "--dp_name", help="Parent data product name."),
    dp_version: Optional[str] = typer.Option(None, "--dp_version", help="Parent data product version (default: v1.0.0)."),
) -> None:
    """Create or update a data contract YAML file in the data mesh."""
    DEFAULT_VERSION = "v1.0.0"

    try:
        dc_spec = read_yaml_spec(path)
        service = get_service()
        dc_id = dc_spec.get("id")

        # RESOLVE parent dp_id if needed
        dp_id = None
        # Resolve parent dp_id ONLY if we are creating a new contract (no ID or ID not in DB)
        dp_id = None
        is_update = dc_id and service.get_data_contract(dc_id)
        if not is_update:
            if dp is not None:
                # Check if dp is a UUID
                try:
                    uuid.UUID(dp)
                    dp_id = dp
                except ValueError:
                    # Treat as path
                    dp_path = Path(dp)
                    dp_spec = read_yaml_spec(dp_path)
                    if "specification" in dp_spec and isinstance(dp_spec["specification"], dict):
                        dp_spec = dp_spec["specification"]
                    d = dp_spec.get("domain", "")
                    n = dp_spec.get("name", "")
                    v = dp_spec.get("version", DEFAULT_VERSION)
                    results = service.list_data_products(domain=d, name=n, version=v)
                    if not results:
                        raise DmPutError(f"No Data Product found for {d}/{n}")
                    dp_id = results[0].id
            elif domain and dp_name:
                d, n, v = domain, dp_name, dp_version or DEFAULT_VERSION
                results = service.list_data_products(domain=d, name=n, version=v)
                if not results:
                    raise DmPutError(f"No Data Product found for {d}/{n}")
                dp_id = results[0].id
            else:
                if dc_id:
                    # If redirected from a failed is_update, tell the user it wasn't found
                    raise DmPutError(f"Data contract {dc_id} not found")
                raise DmPutError("Provide --dp <dp-id-or-path> or --domain and --dp_name for new data contracts.")

        # Create or Update
        new_dc = service.put_data_contract(dc_spec, dp_id=dp_id)
        
        parent_dp = service.get_data_product(new_dc.data_product_id)
        # Record in history
        record_dc(
            dc_id=new_dc.id,
            domain=parent_dp.domain if parent_dp else "unknown",
            name=parent_dp.name if parent_dp else "unknown",
            version=parent_dp.version if parent_dp else "v1.0.0",
        )
        typer.echo(new_dc.id)

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
