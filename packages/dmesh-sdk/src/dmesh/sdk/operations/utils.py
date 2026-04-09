from dmesh.sdk.ports.repository import DataProductRepository
from dmesh.sdk.sdk import AsyncSDK, _RepoWrapper

async def flush(repo: DataProductRepository) -> None:
    """Flush the repository if supported."""
    await AsyncSDK(_RepoWrapper(dp_repo=repo)).flush()
