import typer
from dm.init.errors import (
    ConfigRemoveError,
    ContainerStopError,
    DockerNotAvailableError,
    ImageRemoveError,
    NetworkRemoveError,
)
from dm.init.feedback import ConsoleFeedback
from dm.deinit.orchestrator import DeinitOrchestrator


def deinit(
    full: bool = typer.Option(False, "--full", help="Also remove Docker images after teardown.")
) -> None:
    """Tear down the data mesh environment."""
    feedback = ConsoleFeedback()
    try:
        DeinitOrchestrator(feedback).run(full=full)
    except DockerNotAvailableError as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
    except (ContainerStopError, NetworkRemoveError, ConfigRemoveError, ImageRemoveError) as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
