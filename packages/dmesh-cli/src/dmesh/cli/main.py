import sys
import asyncio

if sys.platform == 'win32':
    # On Windows, psycopg3 (and some other libs) require the SelectorEventLoop
    # instead of the default ProactorEventLoop to run async operations correctly.
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import typer
from dmesh.cli.commands.setup import setup
from dmesh.cli.commands.teardown import teardown
from dmesh.cli.commands.reset import reset
from dmesh.cli.commands.put import app as put_app
from dmesh.cli.commands.get import app as get_app
from dmesh.cli.commands.list import app as list_app
from dmesh.cli.commands.delete import app as delete_app
from dmesh.cli.commands.testdata import app as testdata_app
from dmesh.cli.commands.clean import clean

import os
CLI_NAME = os.environ.get("DMESH_CLI_NAME", "dmesh")
app = typer.Typer(name=CLI_NAME, no_args_is_help=True)
app.command("setup")(setup)
app.command("teardown")(teardown)
app.command("reset")(reset)
app.command("clean")(clean)
app.add_typer(testdata_app, name="testdata")
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


def repl() -> None:
    """Launch the interactive REPL."""
    import shlex
    from rich.console import Console
    from prompt_toolkit import PromptSession
    from prompt_toolkit.formatted_text import HTML
    from prompt_toolkit.history import FileHistory
    import os
    
    console = Console()
    console.print(f"[bold blue]{CLI_NAME} interactive mode[/bold blue]")
    console.print("Type 'exit' or 'quit' to leave. Type '--help' for commands.")
    
    history_file = os.path.join(os.path.expanduser("~"), ".dmesh_history")
    session = PromptSession(history=FileHistory(history_file))
    
    while True:
        try:
            # We use prompt_toolkit to support command history (up/down arrows)
            line = session.prompt(HTML(f"<ansigreen><b>{CLI_NAME}&gt;</b></ansigreen> ")).strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit"):
                break
            
            args = shlex.split(line)
            try:
                # standalone_mode=False prevents Typer from calling sys.exit()
                app(args, standalone_mode=False)
            except SystemExit:
                # Typer raises SystemExit for --help or incorrect arguments
                pass
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Exiting interactive mode.[/yellow]")
            break


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Launch interactive mode.")
) -> None:
    """Data Mesh CLI."""
    if interactive:
        repl()
    elif ctx.invoked_subcommand is None:
        # Show help if no command is provided
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    app()
