import typer
from dmesh.cli.setup.errors import (
    ConfigWriteError,
    ContainerStartError,
    DockerNotAvailableError,
    HealthCheckTimeoutError,
    ImageBuildError,
    ImagePullError,
)
from dmesh.cli.setup.feedback import ConsoleFeedback
from dmesh.cli.setup.orchestrator import SetupOrchestrator

app = typer.Typer()


@app.command()
def setup(flush: bool = typer.Option(False, "--flush", help="Delete all data products after initialisation.")) -> None:
    """Setup the data mesh environment."""
    feedback = ConsoleFeedback()
    try:
        SetupOrchestrator(feedback).run(flush=flush)
    except DockerNotAvailableError as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
    except (ImagePullError, ImageBuildError, ContainerStartError, HealthCheckTimeoutError, ConfigWriteError) as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
