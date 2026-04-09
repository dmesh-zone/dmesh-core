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
            return DMeshService(factory)
            
        # Fallback to in-memory
        from dmesh.sdk.persistency.in_memory import InMemoryRepository
        return DMeshService(InMemoryRepository())
        
    except Exception:
        # Final fallback for misconfigured environments
        from dmesh.sdk.persistency.in_memory import InMemoryRepository
        return DMeshService(InMemoryRepository())
