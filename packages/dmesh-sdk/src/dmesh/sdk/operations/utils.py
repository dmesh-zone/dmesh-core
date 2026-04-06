from dmesh.sdk.ports.repository import DataProductRepository, DataContractRepository

async def flush(repo: DataProductRepository) -> None:
    """Flush the repository if supported."""
    if hasattr(repo, "flush") and callable(getattr(repo, "flush")):
        await repo.flush()
