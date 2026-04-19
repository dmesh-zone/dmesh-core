import asyncio
import typer
from dmesh.cli.utils import get_service

def clean() -> None:
    """Truncate data product and data contract tables."""
    async def _clean():
        async with get_service() as sdk:
            await sdk.clean()
            typer.echo("Data mesh cleaned (all tables truncated).")

    try:
        asyncio.run(_clean())
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
