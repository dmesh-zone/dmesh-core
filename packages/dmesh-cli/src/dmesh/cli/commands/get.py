"""dm get command group."""
import uuid
import asyncio
from typing import Optional
from pathlib import Path

import typer
import yaml

from dmesh.cli.put.history import last_dp, last_dc
from dmesh.cli.utils import get_service

app = typer.Typer(no_args_is_help=True)

DEFAULT_VERSION = "v1.0.0"


def _write_spec(spec: dict, filename: Path) -> Path:
    with filename.open("w") as f:
        yaml.dump(spec, f, default_flow_style=False, allow_unicode=True)
    return filename


def _handle_output(spec: dict, format: str, filename: Path) -> None:
    import json
    if format == "json":
        typer.echo(json.dumps(spec, indent=2))
    elif format == "yaml":
        typer.echo(yaml.dump(spec, default_flow_style=False, allow_unicode=True))
    elif format == "file":
        _write_spec(spec, filename)
        typer.echo(str(filename))
    else:
        raise typer.BadParameter(f"Unsupported format: {format}")


async def _get_dp(
    path: Optional[str] = None,
    domain: Optional[str] = None,
    name: Optional[str] = None,
    version: Optional[str] = None,
    output: str = "yaml",
):
    async with get_service() as service:
        if domain and name:
            ver = version or DEFAULT_VERSION
            results = await service.list_data_products(domain=domain, name=name)
            results = [r for r in results if r["version"] == ver]
            if not results:
                raise ValueError(f"No data product found for domain={domain} name={name} version={ver}")
            _handle_output(results[0], output, Path(f"{domain}_{name}_{ver}.yaml"))
            return

        if path is not None:
            is_uuid = False
            try:
                uuid.UUID(path)
                is_uuid = True
            except ValueError:
                pass

            if is_uuid:
                dp_obj = await service.get_data_product(path, include_metadata=True)
                if not dp_obj:
                    raise ValueError(f"Data product {path} not found.")
                _handle_output(dp_obj.specification, output, Path(f"{dp_obj.domain}_{dp_obj.name}_{dp_obj.version}.yaml"))
                return
            else:
                p = Path(path)
                if not p.exists():
                    raise ValueError(f"File not found: {path}")
                existing = yaml.safe_load(p.read_text()) or {}
                d = existing.get("domain", "")
                n = existing.get("name", "")
                ver = existing.get("version", DEFAULT_VERSION)
                if not d or not n:
                    raise ValueError("YAML file must contain 'domain' and 'name' fields.")
                
                results = await service.list_data_products(domain=d, name=n)
                # results are specs if include_metadata=False
                results = [r for r in results if r["version"] == ver]
                if not results:
                    raise ValueError(f"No data product found for domain={d} name={n} version={ver}")
                
                if output == "file":
                    _write_spec(results[0], p)
                    typer.echo(str(p))
                else:
                    _handle_output(results[0], output, p)
                return

        entry = last_dp()
        if not entry:
            raise ValueError("No history found. Run 'dm put dp' first or provide --domain/--name.")
        
        dp_id = entry["id"]
        dp_obj = await service.get_data_product(dp_id, include_metadata=True)
        if not dp_obj:
            raise ValueError(f"Data product {dp_id} not found in repository.")
            
        _handle_output(dp_obj.specification, output, Path(f"{dp_obj.domain}_{dp_obj.name}_{dp_obj.version}.yaml"))


@app.command("dp")
def dp(
    path: Optional[str] = typer.Argument(None, help="Path to an existing ODPS YAML file to refresh OR a Data Product ID."),
    domain: Optional[str] = typer.Option(None, "--domain", help="Data product domain."),
    name: Optional[str] = typer.Option(None, "--name", help="Data product name."),
    version: Optional[str] = typer.Option(None, "--version", help="Data product version (default: v1.0.0)."),
    output: str = typer.Option("yaml", "--output", "-o", help="Output format: yaml, json, file."),
) -> None:
    """Fetch a data product from the data mesh."""
    try:
        asyncio.run(_get_dp(path, domain, name, version, output))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


async def _get_dc(dc_id: Optional[str], output: str):
    async with get_service() as service:
        if dc_id is None:
            entry = last_dc()
            if not entry:
                raise ValueError("No history found. Provide a DC_ID or run 'dmesh put dc' first.")
            dc_id = entry["id"]

        dc_obj = await service.get_data_contract(dc_id, include_metadata=True)
        if not dc_obj:
            raise ValueError(f"Data contract {dc_id} not found.")

        parent_dp = await service.get_data_product(dc_obj.data_product_id, include_metadata=True)
        domain = parent_dp.domain if parent_dp else "unknown"
        dp_name = parent_dp.name if parent_dp else "unknown"
        dp_version = parent_dp.version if parent_dp else "v1.0.0"
        
        filename = Path(f"{domain}_{dp_name}_{dp_version}_{dc_id}.yaml")
        _handle_output(dc_obj.specification, output, filename)


@app.command("dc")
def dc(
    dc_id: Optional[str] = typer.Argument(None, help="Data contract ID."),
    output: str = typer.Option("yaml", "--output", "-o", help="Output format: yaml, json, file."),
) -> None:
    """Fetch a data contract by ID."""
    try:
        asyncio.run(_get_dc(dc_id, output))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
