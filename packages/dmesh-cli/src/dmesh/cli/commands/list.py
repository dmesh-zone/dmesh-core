"""dm list command group."""
import typer
from typing import Optional

from dmesh.cli.put.errors import ConfigMalformedError, ConfigNotFoundError
from dmesh.cli.utils import get_service

app = typer.Typer(no_args_is_help=True)


@app.command("dps")
def dps() -> None:
    """List all data products sorted by domain, name, version."""
    try:
        service = get_service()
        items = service.list_data_products()
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

    if not items:
        typer.echo("No data products found.")
        return

    def _sort_key(item):
        return (
            item.domain,
            item.name,
            item.version,
        )

    sorted_items = sorted(items, key=_sort_key)

    col_w = {"id": 36, "domain": 20, "name": 30, "version": 12, "status": 12}
    header = (
        f"{'ID':<{col_w['id']}}  "
        f"{'DOMAIN':<{col_w['domain']}}  "
        f"{'NAME':<{col_w['name']}}  "
        f"{'VERSION':<{col_w['version']}}  "
        f"{'STATUS':<{col_w['status']}}"
    )
    typer.echo(header)
    typer.echo("-" * len(header))

    for item in sorted_items:
        typer.echo(
            f"{str(item.id):<{col_w['id']}}  "
            f"{item.domain:<{col_w['domain']}}  "
            f"{item.name:<{col_w['name']}}  "
            f"{item.version:<{col_w['version']}}  "
            f"{'ACTIVE':<{col_w['status']}}"  # Placeholder status
        )


@app.command("dcs")
def dcs(
    domain: Optional[str] = typer.Option(None, "--domain", help="Filter by data product domain."),
    dp_name: Optional[str] = typer.Option(None, "--dp_name", help="Filter by data product name."),
    dp_version: Optional[str] = typer.Option(None, "--dp_version", help="Filter by data product version."),
) -> None:
    """List data contracts with optional data product filters."""
    try:
        service = get_service()
        
        # We need to filter DPs first if filters are provided
        dp_ids = None
        if domain or dp_name or dp_version:
            dps = service.list_data_products(domain=domain, name=dp_name, version=dp_version)
            dp_ids = [dp.id for dp in dps]
            if not dp_ids:
                typer.echo("No data contracts found (no matching data products).")
                return

        all_dcs = []
        if dp_ids is not None:
            for dp_id in dp_ids:
                all_dcs.extend(service.list_data_contracts(dp_id=dp_id))
        else:
            all_dcs = service.list_data_contracts()

        if not all_dcs:
            typer.echo("No data contracts found.")
            return

        col_w = {"dp_id": 36, "domain": 20, "name": 20, "version": 12, "status": 12, "dc_id": 36}
        header = (
            f"{'DP_ID':<{col_w['dp_id']}}  "
            f"{'DP_DOMAIN':<{col_w['domain']}}  "
            f"{'DP_NAME':<{col_w['name']}}  "
            f"{'DP_VERSION':<{col_w['version']}}  "
            f"{'DP_STATUS':<{col_w['status']}}  "
            f"{'DC_ID':<{col_w['dc_id']}}"
        )
        typer.echo(header)
        typer.echo("-" * len(header))
        for dc in all_dcs:
            parent_dp = service.get_data_product(dc.data_product_id)
            typer.echo(
                f"{str(dc.data_product_id):<{col_w['dp_id']}}  "
                f"{parent_dp.domain if parent_dp else 'unknown':<{col_w['domain']}}  "
                f"{parent_dp.name if parent_dp else 'unknown':<{col_w['name']}}  "
                f"{parent_dp.version if parent_dp else 'v1.0.0':<{col_w['version']}}  "
                f"{'ACTIVE':<{col_w['status']}}  "
                f"{str(dc.id):<{col_w['dc_id']}}"
            )
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
