"""dm reset command."""
import typer
from dmesh.cli.setup.feedback import ConsoleFeedback
from dmesh.cli.teardown.orchestrator import TeardownOrchestrator
from dmesh.cli.setup.orchestrator import SetupOrchestrator


def reset(
    full: bool = typer.Option(False, "--full", help="Pass to teardown phase.")
) -> None:
    """Tear down and re-setup the local data mesh environment."""
    feedback = ConsoleFeedback()
    try:
        TeardownOrchestrator(feedback).run(full=full)
        SetupOrchestrator(feedback).run()
    except Exception as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
