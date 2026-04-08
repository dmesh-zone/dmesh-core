import typer
from dmesh.cli.setup.errors import (
    ConfigRemoveError,
    ContainerStopError,
    DockerNotAvailableError,
    ImageRemoveError,
    NetworkRemoveError,
)
from dmesh.cli.setup.feedback import ConsoleFeedback
from dmesh.cli.teardown.orchestrator import TeardownOrchestrator


def teardown(
    full: bool = typer.Option(False, "--full", help="Also remove Docker images after teardown.")
) -> None:
    """Tear down the data mesh environment."""
    feedback = ConsoleFeedback()
    try:
        TeardownOrchestrator(feedback).run(full=full)
    except DockerNotAvailableError as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
    except (ContainerStopError, NetworkRemoveError, ConfigRemoveError, ImageRemoveError) as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
