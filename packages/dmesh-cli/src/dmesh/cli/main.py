import sys
import asyncio

if sys.platform == 'win32':
    # On Windows, psycopg3 (and some other libs) require the SelectorEventLoop
    # instead of the default ProactorEventLoop to run async operations correctly.
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import typer
from dmesh.cli.commands.setup import setup
from dmesh.cli.commands.teardown import teardown
from dmesh.cli.commands.reset import reset
from dmesh.cli.commands.put import app as put_app
from dmesh.cli.commands.get import app as get_app
from dmesh.cli.commands.list import app as list_app
from dmesh.cli.commands.delete import app as delete_app

import os
CLI_NAME = os.environ.get("DMESH_CLI_NAME", "dmesh")
app = typer.Typer(name=CLI_NAME, no_args_is_help=True)
app.command("setup")(setup)
app.command("teardown")(teardown)
app.command("reset")(reset)
app.add_typer(put_app, name="put")
app.add_typer(get_app, name="get")
app.add_typer(list_app, name="list")
app.add_typer(delete_app, name="delete")


@app.command("version")
def version() -> None:
    """Show the CLI version."""
    import importlib.metadata
    v = importlib.metadata.version("dmesh-cli")
    typer.echo(v)


if __name__ == "__main__":
    app()
