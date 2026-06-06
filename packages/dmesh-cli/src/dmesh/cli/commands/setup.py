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
    local_postgres_persistency = "local-postgres-persistency"
    local_rest_persistency_proxy_with_local_postgres_persistency = "local-rest-persistency-proxy-with-local-postgres-persistency"
    local_rest_persistency_proxy_with_local_in_memory_persistency = "local-rest-persistency-proxy-with-local-in-memory-persistency"
    rest_pxy_local_postgres = "rest-pxy-local-postgres"
    rest_pxy_local_mem = "rest-pxy-local-mem"

app = typer.Typer()


@app.command()
def setup(
    flush: bool = typer.Option(False, "--flush", help="Delete all data products after initialisation."),
    rebuild: bool = typer.Option(False, "--rebuild/--no-rebuild", help="Rebuild docker-compose."),
    topology: TopologyChoice = typer.Option(TopologyChoice.local_postgres_persistency, "--topology", help="Setup topology to use.")
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
