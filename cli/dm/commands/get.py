"""dm get command group."""
import uuid
from typing import Optional
from pathlib import Path

import typer
import yaml

from dm.put.errors import ConfigMalformedError, ConfigNotFoundError, DmPutError
from dm.put.history import last_dp, last_dc
from dm.utils import get_service

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
        service = get_service()

        # Mode 1: --domain/--name/--version flags
        if domain and name:
            ver = version or DEFAULT_VERSION
            results = service.list_data_products(domain=domain, name=name, version=ver)
            if not results:
                typer.echo(f"Error: No data product found for domain={domain} name={name} version={ver}", err=True)
                raise typer.Exit(code=1)
            dp_obj = results[0]
            _handle_output(dp_obj.specification, output, Path(f"{domain}_{name}_{ver}.yaml"))
            return

        # Mode 2 & 4: path to existing YAML file OR UUID
        if path is not None:
            # Check if it's a UUID
            try:
                uuid.UUID(path)
                # It's a UUID
                dp_obj = service.get_data_product(path)
                if not dp_obj:
                    typer.echo(f"Error: Data product {path} not found.", err=True)
                    raise typer.Exit(code=1)

                _handle_output(dp_obj.specification, output, Path(f"{dp_obj.domain}_{dp_obj.name}_{dp_obj.version}.yaml"))
                return
            except ValueError:
                # Not a UUID, check if it's a file
                p = Path(path)
                if not p.exists():
                    typer.echo(f"Error: File not found: {path}", err=True)
                    raise typer.Exit(code=1)
                existing = yaml.safe_load(p.read_text()) or {}
                d = existing.get("domain", "")
                n = existing.get("name", "")
                ver = existing.get("version", DEFAULT_VERSION)
                if not d or not n:
                    typer.echo("Error: YAML file must contain 'domain' and 'name' fields.", err=True)
                    raise typer.Exit(code=1)
                
                results = service.list_data_products(domain=d, name=n, version=ver)
                if not results:
                    typer.echo(f"Error: No data product found for domain={d} name={n} version={ver}", err=True)
                    raise typer.Exit(code=1)
                
                dp_obj = results[0]
                if output == "file":
                    _write_spec(dp_obj.specification, p)
                    typer.echo(str(p))
                else:
                    _handle_output(dp_obj.specification, output, p)
                return

        # Mode 3: use last dp from history
        entry = last_dp()
        if not entry:
            typer.echo(
                "Error: No history found. Run 'dm put dp' first or provide --domain/--name.",
                err=True,
            )
            raise typer.Exit(code=1)
        dp_id = entry["id"]
        dp_obj = service.get_data_product(dp_id)
        if not dp_obj:
            typer.echo(f"Error: Data product {dp_id} not found in repository.", err=True)
            raise typer.Exit(code=1)
            
        _handle_output(dp_obj.specification, output, Path(f"{dp_obj.domain}_{dp_obj.name}_{dp_obj.version}.yaml"))

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


@app.command("dc")
def dc(
    dc_id: Optional[str] = typer.Argument(None, help="Data contract ID."),
    output: str = typer.Option("yaml", "--output", "-o", help="Output format: yaml, json, file."),
) -> None:
    """Fetch a data contract by ID."""
    try:
        service = get_service()

        if dc_id is None:
            entry = last_dc()
            if not entry:
                typer.echo("Error: No history found. Provide a DC_ID or run 'odm put dc' first.", err=True)
                raise typer.Exit(code=1)
            dc_id = entry["id"]

        dc_obj = service.get_data_contract(dc_id)
        if not dc_obj:
            typer.echo(f"Error: Data contract {dc_id} not found.", err=True)
            raise typer.Exit(code=1)

        parent_dp = service.get_data_product(dc_obj.data_product_id)
        domain = parent_dp.domain if parent_dp else "unknown"
        dp_name = parent_dp.name if parent_dp else "unknown"
        dp_version = parent_dp.version if parent_dp else "v1.0.0"
        
        filename = Path(f"{domain}_{dp_name}_{dp_version}_{dc_id}.yaml")
        _handle_output(dc_obj.specification, output, filename)

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
