"""dm get dc subcommand — fetch a data contract by id."""
from pathlib import Path

import httpx
import typer
import yaml

from dmesh.cli.put.errors import DmPutError
from dmesh.sdk.config import get_settings


def get_dc(
    dc_id: str = typer.Argument(..., help="Data contract ID."),
) -> None:
    """Fetch a data contract by ID and write it to a YAML file."""
    settings = get_settings()
    rest_url = settings.sdk.rest_persistency_proxy_url
    ws = f"{rest_url.rstrip('/')}/{settings.api.base_path.strip('/')}"
    if rest_url == "http://0.0.0.0:8000":
        ws = f"http://localhost:8000/{settings.api.base_path.strip('/')}"

    try:
        resp = httpx.get(f"{ws}/dcs/{dc_id}", timeout=30)
    except httpx.RequestError as e:
        typer.echo(f"Error: WS layer is unreachable: {e}", err=True)
        raise typer.Exit(code=1)

    if resp.status_code == 404:
        typer.echo(f"Error: Data contract {dc_id} not found.", err=True)
        raise typer.Exit(code=1)
    if resp.status_code != 200:
        typer.echo(f"Error: WS layer returned HTTP {resp.status_code}", err=True)
        raise typer.Exit(code=1)

    spec = resp.json()
    domain = spec.get("domain", "unknown")
    dp_name = spec.get("name", "unknown")
    out = Path(f"{domain}_{dp_name}_{dc_id}.yaml")
    with out.open("w") as f:
        yaml.dump(spec, f, default_flow_style=False, allow_unicode=True)
    typer.echo(str(out))
