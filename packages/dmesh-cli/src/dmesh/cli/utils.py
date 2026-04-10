from dmesh.sdk import AsyncSDK
from dmesh.sdk.config import get_settings
from dmesh.sdk.persistency.factory import RepositoryFactory

def get_service() -> AsyncSDK:
    """
    Initializes and returns an AsyncSDK instance using the unified configuration.
    """
    try:
        settings = get_settings()
        
        # Use factory to create appropriate repositories
        # Default to postgres if host is provided, else in-memory
        db_type = "postgres" if settings.db.host else "memory"
        factory = RepositoryFactory().create_from_settings(settings, db_type=db_type)
        return AsyncSDK(factory)
            
    except Exception:
        # Final fallback for misconfigured environments: in-memory factory
        factory = RepositoryFactory().create(db_type="memory")
        return AsyncSDK(factory)
