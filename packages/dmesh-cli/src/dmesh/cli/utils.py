from dmesh.sdk import AsyncSDK
from dmesh.sdk.config import get_settings
from dmesh.sdk.persistency.factory import RepositoryFactory

def get_service() -> AsyncSDK:
    """
    Initializes and returns an AsyncSDK instance using the unified configuration.
    """
    settings = get_settings()
    
    # Use factory to create appropriate repositories
    # Default to postgres if host is provided, else in-memory
    db_type = "postgres" if settings.db.host else "memory"
    
    if getattr(settings.sdk, "filesystem_persistency", False):
        import typer
        root_dir = getattr(settings.sdk, "data_products_filesystem_root", "tmp/data_products_filesystem_root")
        typer.echo(f"📁 Using Filesystem Backend ({root_dir})")
    elif getattr(settings.sdk, "rest_persistency_proxy", False):
        import typer
        proxy_url = getattr(settings.sdk, "rest_persistency_proxy_url", "http://0.0.0.0:8000")
        typer.echo(f"🔌 Using REST API Backend ({proxy_url})")
    else:
        import typer
        typer.echo(f"🗄️ Using Database Backend ({db_type})")
        
    factory = RepositoryFactory().create_from_settings(settings, db_type=db_type)
    return AsyncSDK(factory)
