import typer
from dm.init.errors import (
    ConfigWriteError,
    ContainerStartError,
    DockerNotAvailableError,
    HealthCheckTimeoutError,
    ImageBuildError,
    ImagePullError,
)
from dm.init.feedback import ConsoleFeedback
from dm.init.orchestrator import InitOrchestrator

app = typer.Typer()


@app.command()
def init(flush: bool = typer.Option(False, "--flush", help="Delete all data products after initialisation.")) -> None:
    """Initialise the data mesh environment."""
    feedback = ConsoleFeedback()
    try:
        InitOrchestrator(feedback).run(flush=flush)
    except DockerNotAvailableError as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
    except (ImagePullError, ImageBuildError, ContainerStartError, HealthCheckTimeoutError, ConfigWriteError) as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
