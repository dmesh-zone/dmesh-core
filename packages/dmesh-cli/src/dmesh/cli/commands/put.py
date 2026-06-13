"""dm put command group."""
from pathlib import Path
from typing import Optional
import uuid
import asyncio

import typer
import yaml

from dmesh.cli.put.errors import DmPutError
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
        if isinstance(dp_obj, dict):
            dp_id = dp_obj.get("id")
            domain = dp_obj.get("domain")
            name = dp_obj.get("name")
            version = dp_obj.get("version")
        else:
            dp_id = dp_obj.id
            domain = dp_obj.domain
            name = dp_obj.name
            version = dp_obj.version
            
        record_dp(
            dp_id=str(dp_id) if dp_id else "unknown",
            domain=str(domain) if domain else "unknown",
            name=str(name) if name else "unknown",
            version=str(version) if version else "unknown",
        )
        return str(dp_id) if dp_id else "unknown"


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
):
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
                    results = await service.list_data_products(domain=d, name=n)
                    if not results:
                        raise DmPutError(f"No Data Product found for {d}/{n}")
                    
                    first = results[0]
                    dp_id = first.get("id") if isinstance(first, dict) else first.id
            elif domain and dp_name:
                d, n = domain, dp_name
                results = await service.list_data_products(domain=d, name=n)
                if not results:
                    raise DmPutError(f"No Data Product found for {d}/{n}")
                
                first = results[0]
                dp_id = first.get("id") if isinstance(first, dict) else first.id
            else:
                if dc_id:
                    raise DmPutError(f"Data contract {dc_id} not found")
                raise DmPutError("Provide --dp <dp-id-or-path> or --domain and --dp_name for new data contracts.")

        # Create or Update
        new_dc = await service.put_data_contract(dc_spec, dp_id=str(dp_id) if dp_id else None, include_metadata=True)
        
        dc_id = new_dc.get("id") if isinstance(new_dc, dict) else new_dc.id
        dc_dp_id = new_dc.get("data_product_id") if isinstance(new_dc, dict) else new_dc.data_product_id
        
        parent_dp = await service.get_data_product(str(dc_dp_id) if dc_dp_id else "", include_metadata=True)
        
        if isinstance(parent_dp, dict):
            dp_domain = parent_dp.get("domain", "unknown")
            dp_name = parent_dp.get("name", "unknown")
            dp_version = parent_dp.get("version", "v1.0.0")
        elif parent_dp:
            dp_domain = parent_dp.domain
            dp_name = parent_dp.name
            dp_version = parent_dp.version
        else:
            dp_domain = "unknown"
            dp_name = "unknown"
            dp_version = "v1.0.0"
            
        # Record in history
        record_dc(
            dc_id=str(dc_id) if dc_id else "unknown",
            domain=str(dp_domain) if dp_domain else "unknown",
            name=str(dp_name) if dp_name else "unknown",
            version=str(dp_version) if dp_version else "unknown",
        )
        return str(dc_id) if dc_id else "unknown"


@app.command("dc")
def dc(
    path: Path = typer.Argument(..., help="Path to the ODCS data contract YAML file."),
    dp: Optional[str] = typer.Option(None, "--dp", help="Path to or ID of the parent data product."),
    domain: Optional[str] = typer.Option(None, "--domain", help="Parent data product domain."),
    dp_name: Optional[str] = typer.Option(None, "--dp_name", help="Parent data product name."),
) -> None:
    """Create or update a data contract YAML file in the data mesh."""
    try:
        dc_id = asyncio.run(_put_dc(path, dp, domain, dp_name))
        typer.echo(dc_id)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
