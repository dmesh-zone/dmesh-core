from dmesh.sdk import DMeshService
from dmesh.sdk.config import get_settings
from dmesh.sdk.persistency.factory import RepositoryFactory

def get_service() -> DMeshService:
    """
    Initializes and returns a DMeshService instance using the unified configuration.
    """
    try:
        settings = get_settings()
        
        # If db.host is provided, use Postgres (Sync for CLI)
        if settings.db.host:
            factory = RepositoryFactory().create_from_settings(settings, db_type="postgres_sync")
            dp_repo = factory.get_data_product_repository()
            dc_repo = factory.get_data_contract_repository()
            return DMeshService(dp_repo, dc_repo)
            
        # Fallback to in-memory
        from dmesh.sdk.persistency.in_memory import SyncInMemoryDataProductRepository, SyncInMemoryDataContractRepository
        repo = SyncInMemoryDataProductRepository({})
        return DMeshService(repo, repo)
        
    except Exception:
        # Final fallback for misconfigured environments
        from dmesh.sdk.persistency.in_memory import SyncInMemoryDataProductRepository, SyncInMemoryDataContractRepository
        repo = SyncInMemoryDataProductRepository({})
        return DMeshService(repo, repo)