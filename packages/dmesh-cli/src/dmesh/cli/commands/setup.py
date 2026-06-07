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
from enum import Enum

class TopologyChoice(str, Enum):
    docker_postgres = "docker-postgres"
    docker_rest_pxy_postgres = "docker-rest-pxy-postgres"
    docker_rest_pxy_mem = "docker-rest-pxy-mem"
    databricks_rest_pxy = "databricks-rest-pxy"

app = typer.Typer()


@app.command()
def setup(
    flush: bool = typer.Option(False, "--flush", help="Delete all data products after initialisation."),
    rebuild: bool = typer.Option(False, "--rebuild/--no-rebuild", help="Rebuild docker-compose."),
    topology: TopologyChoice = typer.Option(TopologyChoice.docker_postgres, "--topology", help="Setup topology to use.")
) -> None:
    """Setup the data mesh environment."""
    feedback = ConsoleFeedback()
    import asyncio
    try:
        asyncio.run(SetupOrchestrator(feedback).run(flush=flush, rebuild=rebuild, topology=topology.value))
    except DockerNotAvailableError as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
    except (ImagePullError, ImageBuildError, ContainerStartError, HealthCheckTimeoutError, ConfigWriteError) as e:
        feedback.error(str(e))
        raise typer.Exit(code=1)
