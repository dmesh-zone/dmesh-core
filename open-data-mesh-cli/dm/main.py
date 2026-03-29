import typer
from dm.commands.init import init
from dm.commands.deinit import deinit
from dm.commands.reset import reset
from dm.commands.put import app as put_app
from dm.commands.get import app as get_app
from dm.commands.list import app as list_app
from dm.commands.delete import app as delete_app

import os
CLI_NAME = os.environ.get("ODM_CLI_NAME", "odm")
app = typer.Typer(name=CLI_NAME, no_args_is_help=True)
app.command("init")(init)
app.command("deinit")(deinit)
app.command("reset")(reset)
app.add_typer(put_app, name="put")
app.add_typer(get_app, name="get")
app.add_typer(list_app, name="list")
app.add_typer(delete_app, name="delete")


@app.command("version")
def version() -> None:
    """Show the CLI version."""
    import importlib.metadata
    v = importlib.metadata.version("open-data-mesh-cli")
    typer.echo(v)


if __name__ == "__main__":
    app()
