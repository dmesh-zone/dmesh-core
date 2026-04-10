"""dm put command group."""
from pathlib import Path
from typing import Optional
import uuid
import asyncio

import typer
import yaml

from dmesh.cli.put.errors import DmPutError, ConfigMalformedError, ConfigNotFoundError
from dmesh.cli.put.errors import FileNotFoundError as DmFileNotFoundError
from dmesh.cli.put.errors import YamlParseError
from dmesh.cli.put.history import record_dp, record_dc
from dmesh.cli.utils import get_service

app = typer.Typer(no_args_is_help=True)


def read_yaml_spec(path: Path) -> dict:
    """Read and parse a YAML file into a dict."""
    if not path.exists():
        raise DmFileNotFoundError(f"File not found: {path}")
    try:
        return yaml.safe_load(path.read_text()) or {}
    except yaml.YAMLError as e:
        raise YamlParseError(f"Failed to parse YAML: {e}") from e


async def _put_dp(path: Path):
    spec = read_yaml_spec(path)
    async with get_service() as service:
        dp_obj = await service.put_data_product(spec, include_metadata=True)
        record_dp(
            dp_id=dp_obj.id,
            domain=dp_obj.domain,
            name=dp_obj.name,
            version=dp_obj.version,
        )
        return dp_obj.id


@app.command("dp")
def dp(
    path: Path = typer.Argument(..., help="Path to the ODPS data product YAML file."),
) -> None:
    """Publish a data product YAML file to the data mesh."""
    try:
        dp_id = asyncio.run(_put_dp(path))
        typer.echo(dp_id)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


async def _put_dc(
    path: Path,
    dp: Optional[str] = None,
    domain: Optional[str] = None,
    dp_name: Optional[str] = None,
    dp_version: Optional[str] = None,
):
    DEFAULT_VERSION = "v1.0.0"
    dc_spec = read_yaml_spec(path)
    dc_id = dc_spec.get("id")

    async with get_service() as service:
        # RESOLVE parent dp_id if needed
        dp_id = None
        is_update = dc_id and await service.get_data_contract(dc_id)
        if not is_update:
            if dp is not None:
                try:
                    uuid.UUID(dp)
                    dp_id = dp
                except ValueError:
                    dp_path = Path(dp)
                    dp_spec = read_yaml_spec(dp_path)
                    if "specification" in dp_spec and isinstance(dp_spec["specification"], dict):
                        dp_spec = dp_spec["specification"]
                    d = dp_spec.get("domain", "")
                    n = dp_spec.get("name", "")
                    v = dp_spec.get("version", DEFAULT_VERSION)
                    results = await service.list_data_products(domain=d, name=n)
                    # Filter by version manually if needed or update list_data_products
                    results = [r for r in results if r.version == v]
                    if not results:
                        raise DmPutError(f"No Data Product found for {d}/{n}")
                    dp_id = results[0].id
            elif domain and dp_name:
                d, n, v = domain, dp_name, dp_version or DEFAULT_VERSION
                results = await service.list_data_products(domain=d, name=n)
                results = [r for r in results if r.version == v]
                if not results:
                    raise DmPutError(f"No Data Product found for {d}/{n}")
                dp_id = results[0].id
            else:
                if dc_id:
                    raise DmPutError(f"Data contract {dc_id} not found")
                raise DmPutError("Provide --dp <dp-id-or-path> or --domain and --dp_name for new data contracts.")

        # Create or Update
        new_dc = await service.put_data_contract(dc_spec, dp_id=dp_id, include_metadata=True)
        
        parent_dp = await service.get_data_product(new_dc.data_product_id, include_metadata=True)
        # Record in history
        record_dc(
            dc_id=new_dc.id,
            domain=parent_dp.domain if parent_dp else "unknown",
            name=parent_dp.name if parent_dp else "unknown",
            version=parent_dp.version if parent_dp else "v1.0.0",
        )
        return new_dc.id


@app.command("dc")
def dc(
    path: Path = typer.Argument(..., help="Path to the ODCS data contract YAML file."),
    dp: Optional[str] = typer.Option(None, "--dp", help="Path to or ID of the parent data product."),
    domain: Optional[str] = typer.Option(None, "--domain", help="Parent data product domain."),
    dp_name: Optional[str] = typer.Option(None, "--dp_name", help="Parent data product name."),
    dp_version: Optional[str] = typer.Option(None, "--dp_version", help="Parent data product version (default: v1.0.0)."),
) -> None:
    """Create or update a data contract YAML file in the data mesh."""
    try:
        dc_id = asyncio.run(_put_dc(path, dp, domain, dp_name, dp_version))
        typer.echo(dc_id)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
