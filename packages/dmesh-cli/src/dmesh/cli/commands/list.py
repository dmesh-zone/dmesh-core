"""dm list command group."""
import typer
import asyncio
from typing import Optional

from dmesh.cli.utils import get_service

app = typer.Typer(no_args_is_help=True)


async def _list_dps():
    async with get_service() as service:
        items = await service.list_data_products(include_metadata=True)
        if not items:
            typer.echo("No data products found.")
            return

        sorted_items = sorted(items, key=lambda x: (
            x.get("domain", "") if isinstance(x, dict) else x.domain,
            x.get("name", "") if isinstance(x, dict) else x.name,
            x.get("version", "") if isinstance(x, dict) else x.version
        ))

        col_w = {"domain": 20, "name": 30, "id": 36}
        header = (
            f"{'DOMAIN':<{col_w['domain']}}  "
            f"{'NAME':<{col_w['name']}}  "
            f"{'ID':<{col_w['id']}}"
        )
        typer.echo(header)
        typer.echo("-" * len(header))

        for item in sorted_items:
            if isinstance(item, dict):
                i_domain = item.get("domain", "")
                i_name = item.get("name", "")
                i_id = item.get("id", "")
            else:
                i_domain = item.domain
                i_name = item.name
                i_id = item.id
                
            i_domain_str = str(i_domain) if i_domain else "undefined"
                
            typer.echo(
                f"{i_domain_str:<{col_w['domain']}}  "
                f"{str(i_name):<{col_w['name']}}  "
                f"{str(i_id):<{col_w['id']}}"
            )


@app.command("dps")
def dps() -> None:
    """List all data products sorted by domain, name, version."""
    try:
        asyncio.run(_list_dps())
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)


async def _list_dcs(domain: Optional[str], dp_name: Optional[str]):
    async with get_service() as service:
        dp_ids = None
        if domain or dp_name:
            kwargs: dict = {"include_metadata": True}
            if domain is not None:
                kwargs["domain"] = domain
            if dp_name is not None:
                kwargs["name"] = dp_name
            dps = await service.list_data_products(**kwargs)
            
            dp_ids = []
            for dp in dps:
                dp_id = dp.get("id") if isinstance(dp, dict) else dp.id
                if dp_id is not None:
                    dp_ids.append(str(dp_id))
                    
            if not dp_ids:
                typer.echo("No data contracts found (no matching data products).")
                return

        all_dcs = []
        if dp_ids is not None:
            for dp_id in dp_ids:
                all_dcs.extend(await service.list_data_contracts(dp_id=dp_id, include_metadata=True))
        else:
            all_dcs = await service.list_data_contracts(include_metadata=True)

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
            dc_dp_id = dc.get("data_product_id") if isinstance(dc, dict) else dc.data_product_id
            dc_id = dc.get("id") if isinstance(dc, dict) else dc.id
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
                
            typer.echo(
                f"{str(dc_dp_id):<{col_w['dp_id']}}  "
                f"{str(dp_domain):<{col_w['domain']}}  "
                f"{str(dp_name):<{col_w['name']}}  "
                f"{str(dp_version):<{col_w['version']}}  "
                f"{'ACTIVE':<{col_w['status']}}  "
                f"{str(dc_id):<{col_w['dc_id']}}"
            )


@app.command("dcs")
def dcs(
    domain: Optional[str] = typer.Option(None, "--domain", help="Filter by data product domain."),
    dp_name: Optional[str] = typer.Option(None, "--dp_name", help="Filter by data product name."),
) -> None:
    """List data contracts with optional data product filters."""
    try:
        asyncio.run(_list_dcs(domain, dp_name))
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
