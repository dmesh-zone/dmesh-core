import uuid
import typer
from dm.utils import get_service

app = typer.Typer(help="Delete data products or data contracts.", no_args_is_help=True)

@app.command("dp")
def delete_dp(
    id: uuid.UUID = typer.Argument(..., help="Data product ID to delete.")
) -> None:
    """Delete a data product by ID."""
    try:
        service = get_service()
        success = service.delete_data_product(str(id))
        if success:
            typer.echo(f"Data product {id} deleted.")
        else:
            typer.echo(f"Error: Data product {id} not found.", err=True)
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

@app.command("dc")
def delete_dc(
    id: uuid.UUID = typer.Argument(..., help="Data contract ID to delete.")
) -> None:
    """Delete a data contract by ID."""
    try:
        service = get_service()
        success = service.delete_data_contract(str(id))
        if success:
            typer.echo(f"Data contract {id} deleted.")
        else:
            typer.echo(f"Error: Data contract {id} not found.", err=True)
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
