"""dm reset command."""
import typer
from dmesh.cli.init.feedback import ConsoleFeedback
from dmesh.cli.deinit.orchestrator import DeinitOrchestrator
from dmesh.cli.init.orchestrator import InitOrchestrator


def reset(
    full: bool = typer.Option(False, "--full", help="Legacy option, not used in SQLite mode.")
) -> None:
    """Tear down and reinitialise the local data mesh environment."""
    feedback = ConsoleFeedback()
    try:
        DeinitOrchestrator(feedback).run(full=full)
        InitOrchestrator(feedback).run()
    except Exception as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
